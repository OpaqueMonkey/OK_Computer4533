#!/usr/bin/env python3
"""
Minify index.html -> page.min.html for onchain upload.

Edit index.html (readable). Run `python3 build.py`. Upload page.min.html.

Onchain pages are billed per byte of storage, so the readable source is the
thing you maintain and the minified file is the thing you pay for. Nothing
here changes behaviour: comments and whitespace go, code does not.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
# source -> upload artifact
TARGETS = {"index.html": "page.min.html", "lite.html": "lite.min.html",
           "test.html": "test.min.html"}


def strip_js_comments(js: str) -> str:
    """Remove // and /* */ comments while respecting string literals.

    A plain regex would corrupt "https://..." inside strings, so walk the
    source tracking quote state instead.
    """
    out, i, n = [], 0, len(js)
    quote = None
    while i < n:
        c = js[i]
        if quote:
            out.append(c)
            if c == "\\" and i + 1 < n:      # escape: copy the next char verbatim
                out.append(js[i + 1]); i += 2; continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in "\"'`":
            quote = c; out.append(c); i += 1; continue
        if c == "/" and i + 1 < n and js[i + 1] == "/":
            while i < n and js[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and js[i + 1] == "*":
            j = js.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        out.append(c); i += 1
    return "".join(out)


def minify_js(js: str) -> str:
    js = strip_js_comments(js)
    lines = [ln.strip() for ln in js.split("\n")]
    # Keep line breaks: joining everything risks automatic-semicolon-insertion
    # bugs, and newlines cost 1 byte each.
    return "\n".join(ln for ln in lines if ln)


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    # #aabbcc -> #abc where the pairs repeat
    css = re.sub(r"#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3\b",
                 r"#\1\2\3", css, flags=re.I)
    return css.strip()


def minify_html(html: str) -> str:
    html = re.sub(r"<!--(?!\[if).*?-->", "", html, flags=re.S)
    # Indentation between tags is dead weight; a newline inside running text
    # is a real word separator. Distinguish the two.
    html = re.sub(r">\s*\n\s*<", "><", html)
    html = re.sub(r"\s*\n\s*", " ", html)
    return html.strip()


def build(src_name: str, out_name: str) -> None:
    src_path, out_path = HERE / src_name, HERE / out_name
    if not src_path.exists():
        return
    src = src_path.read_text(encoding="utf-8")

    style = re.search(r"<style>(.*?)</style>", src, re.S)
    script = re.search(r"<script>(.*?)</script>", src, re.S)

    out = src
    if style:
        out = out.replace(style.group(0), "\x00CSS\x00")
    if script:
        out = out.replace(script.group(0), "\x00JS\x00")
    out = minify_html(out)
    if style:
        out = out.replace("\x00CSS\x00", "<style>" + minify_css(style.group(1)) + "</style>")
    if script:
        out = out.replace("\x00JS\x00", "<script>" + minify_js(script.group(1)) + "</script>")

    out_path.write_text(out, encoding="utf-8")
    before, after = len(src.encode()), len(out.encode())
    print(f"{src_name:<12} {before:>7,} -> {out_name:<14} {after:>7,} bytes")


def main() -> int:
    for src_name, out_name in TARGETS.items():
        build(src_name, out_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

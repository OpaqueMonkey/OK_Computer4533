# $BNKRBUD

Onchain landing page for $BNKRBUD, a token on Base launched via pools.fun.
95% of the deployer's trading fees buy $BNKR on the open market and burn it.

Mascot is **OK Computer #4533**, drawn as a 32x32 pixel sprite in code.

## Files

| file            | what it is                                              |
| --------------- | ------------------------------------------------------- |
| `index.html`    | readable source — **edit this**                          |
| `build.py`      | minifier                                                 |
| `page.min.html` | generated upload artifact — **paste this onchain**       |

```
python3 build.py
```

## Why there's a build step

Uploading the unminified 37KB file reverted with `status: false` and
`gasUsed: 16777216` — exactly 2^24, and an out-of-gas revert carries no
reason string. At the standard 20,000 gas per 32-byte word (~625 gas/byte),
37,574 bytes needs roughly 23.5M gas against a 16.78M limit.

Note that `cumulativeGasUsed` on that same block was 37.6M, so 2^24 is a
**transaction** gas cap in the uploader, not a protocol limit. If the tool
lets you raise it, that is the other way out.

Current: **23,215 bytes**, roughly 14.5M gas — about 13% under the cap.

The 64KB platform limit is a *storage* ceiling. Gas binds first. Keep the
minified output under ~24KB.

## Before launch

Two constants at the top of the `<script>` in `index.html`:

- `POOL` — the pools.fun URL. Empty, the buy buttons show a "not live yet"
  toast instead of dead-linking.
- `IMG` — optional Base64 data URI of the real NFT art, replacing the drawn
  sprite. Export at 32x32; the 512x512 PNG costs several KB of gas.

Re-run `python3 build.py` after either.

## Constraints

No external dependencies: inline CSS, inline JS, no image files, system
fonts only. The only outbound URLs are hyperlinks (bankr.bot, opensea.io).
Verified rendering at 1000px and 390px with no console errors and no
horizontal overflow.

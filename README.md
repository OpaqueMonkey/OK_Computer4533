# $BNKRBUD

Onchain landing page for $BNKRBUD (`0x07ad3ece2e21778b9fab7d950bec96a1b43bee96`),
a token on Base launched via pools.fun. 95% of the deployer's trading fees buy
$BNKR on the open market and burn it.

Mascot is **OK Computer #4533**, drawn as a 32x32 pixel sprite in code.

## Files

| source       | upload artifact | bytes  | what it is                          |
| ------------ | --------------- | ------ | ----------------------------------- |
| `index.html` | `page.min.html` | 23,468 | the full page                       |
| `lite.html`  | `lite.min.html` | 7,029  | stripped: Bud, pitch, links only    |
| `test.html`  | `test.min.html` | 487    | a probe, to test the upload at all  |

```
python3 build.py        # minifies all three
```

## Upload status: blocked, cause not yet established

Two upload attempts have reverted. Both receipts:

| | attempt 1 | attempt 2 | ratio |
| --- | ---: | ---: | ---: |
| page bytes | 37,574 | 23,468 | 0.625 |
| `l1GasUsed` | 240,591 | 161,385 | 0.671 |
| `blobGasUsed` | 2,225,328 | 1,492,728 | 0.671 |
| **`gasUsed`** | **16,777,216** | **16,777,216** | **1.000** |

L1 and blob gas both scaled down with the payload, so the smaller file
genuinely reached the chain. But `gasUsed` is bit-identical at exactly
2^24 — a round power of two, i.e. a gas *limit* being consumed whole,
which is the out-of-gas signature (`status:false` with no revert reason).

**A 37.5% smaller page moved execution gas by zero.** If per-byte storage
cost were the binding constraint, it would have fallen proportionally like
the other two. So the earlier "just make it smaller" theory is not
supported by the evidence, and shrinking further may not help.

Note `cumulativeGasUsed` was 37.6M and 47.9M on those blocks, so 2^24 is a
**transaction** cap in the uploader, not a protocol limit.

### Narrowing it down

Upload `test.min.html` (487 bytes) first. It splits the remaining
possibilities cleanly:

- **It uploads** — size is the axis after all, and the threshold sits
  somewhere under 23KB. Try `lite.min.html` (7KB) next, then `page.min.html`.
- **It fails identically**, still burning exactly 16,777,216 — the page
  content is irrelevant and no amount of shrinking will fix it. The cause is
  the transaction or the contract call: wrong entry point, an upload that
  expects to be chunked across several transactions, or a gas cap set too
  low for any write.

In the second case, worth asking the platform:

1. Is a page written in one transaction, or appended in chunks?
2. What gas limit does the uploader set, and can it be raised?
3. What is the largest page anyone has successfully stored?

Investigation from here was limited by network policy: this environment
blocks egress to basescan.org, pools.fun, dexscreener and every public Base
RPC, so the contract at `0x04d7c8b512d5455e20df1e808f12cad1e3d766e5` could
not be inspected, gas could not be estimated, and the real revert reason
could not be recovered.

## Before launch

`IMG` at the top of the `<script>` in `index.html` optionally takes a Base64
data URI of the real NFT art in place of the drawn sprite. Export at 32x32 —
the 512x512 PNG costs several KB. Re-run `python3 build.py` after editing.

## Constraints

No external dependencies: inline CSS, inline JS, no image files, system
fonts only. The only outbound URLs are hyperlinks (pools.fun, bankr.bot,
opensea.io). All three pages verified rendering with no console errors and
no horizontal overflow.

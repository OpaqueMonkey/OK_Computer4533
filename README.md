# $BNKRBUD

Onchain landing page for $BNKRBUD (`0x07ad3ece2e21778b9fab7d950bec96a1b43bee96`),
a token on Base launched via pools.fun. 95% of the deployer's trading fees buy
$BNKR on the open market and burn it.

Mascot is **OK Computer #4533**, drawn as a 32x32 pixel sprite in code.

## Upload this one

`lite.min.html` — **7,381 bytes**, under the 8,221-byte page known to upload.

| source       | artifact        |  bytes | status                        |
| ------------ | --------------- | -----: | ----------------------------- |
| `lite.html`  | `lite.min.html` |  7,381 | **upload this**               |
| `test.html`  | `test.min.html` |    487 | bare probe, if lite ever fails |
| `index.html` | `page.min.html` | 23,468 | too big — reverted            |

```
python3 build.py        # minifies every source in TARGETS
```

## The size ceiling is gas, not the stated 64KB

Uploads are capped by a per-transaction gas limit of 16,777,216 (2^24), not
by the platform's advertised 64KB. Two data points bound the real cost:

| page bytes | result | implies |
| ---------: | ------ | ------- |
| 8,221 | uploaded | cost <= 2,041 gas/byte |
| 23,468 | reverted | cost > 715 gas/byte |
| 37,574 | reverted | — |

Both failures show `status:false`, no revert reason, and `gasUsed` exactly
16,777,216 — the out-of-gas signature, where the transaction consumes its
whole limit.

Between the two failures the page shrank 37.5% and `l1GasUsed` /
`blobGasUsed` both fell to ~67%, but `gasUsed` stayed bit-identical. That
is consistent with running out of gas at *both* sizes; it does not mean
size is irrelevant. An earlier estimate of 625 gas/byte here was simply too
low, which is why 23,468 bytes still failed.

**Keep the built file under ~8,000 bytes.** That is the only figure backed
by a successful upload. Anything larger is untested and may revert.

Note `cumulativeGasUsed` on those blocks was 37.6M and 47.9M, so 2^24 is a
cap in the uploader, not a protocol limit. If it can be raised, a larger
page becomes possible and `page.min.html` is ready for that.

## Constraints

No external dependencies: inline `<style>`, inline `<script>`, no image
files, system fonts only. The only outbound URLs are hyperlinks (pools.fun,
bankr.bot, opensea.io).

The sprite is drawn to a `<canvas>` from a text grid rather than embedded as
a Base64 image — cheaper, and sharp at any size.

`lite.min.html` is pure ASCII apart from a few punctuation characters. The
larger `page.min.html` contains a 4-byte emoji, which is untested against
this uploader.

## Before launch

`IMG` at the top of the `<script>` in `index.html` optionally takes a Base64
data URI of the real NFT art in place of the drawn sprite. Export at 32x32.
Re-run `python3 build.py` after editing.

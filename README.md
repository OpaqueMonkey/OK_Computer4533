# $BNKRBUD

Onchain landing page for $BNKRBUD (`0x07ad3ece2e21778b9fab7d950bec96a1b43bee96`),
a token on Base launched via pools.fun.

Mascot is **OK Computer #4533**, drawn as a 32x32 pixel sprite in code.

## Files

| file            | what it is                                    |
| --------------- | --------------------------------------------- |
| `index.html`    | readable source — **edit this**               |
| `build.py`      | minifier                                      |
| `page.min.html` | generated — **upload this** (7,796 bytes)     |

```
python3 build.py
```

## Fee mechanics on the page

**ETH fee income**

- 50% — buy & burn $BNKR: spot buy pressure, permanent reduction of circulating float
- 40% — $BNKR/ETH liquidity: deepens pool depth
- 10% — agent ops: gas, compute and tooling for onchain activity

**$BNKRBUD fee income** — tipped out on Twitter and airdropped to $BNKRBUD holders.

The page states the splits and their direct effects only. Claims that
depend on unverified implementation details (how dev incentives tie to LP
volume, whether deeper liquidity stabilises volatility) are deliberately
left off.

## Size ceiling: keep the build under ~8,000 bytes

Uploads are capped by a per-transaction gas limit of 16,777,216 (2^24), not
by the platform's advertised 64KB. Three data points:

| page bytes | result   | implies                |
| ---------: | -------- | ---------------------- |
|      8,221 | uploaded | cost <= 2,041 gas/byte |
|     23,468 | reverted | cost > 715 gas/byte    |
|     37,574 | reverted | —                      |

Both failures showed `status:false`, no revert reason, and `gasUsed`
exactly 16,777,216 — the out-of-gas signature, where the transaction burns
its whole limit.

8,221 bytes is the only size backed by a successful upload, so treat ~8,000
as the ceiling. `build.py` prints the byte count on every run; if it creeps
past that, cut content rather than hoping.

`cumulativeGasUsed` on those blocks was 37.6M and 47.9M, so 2^24 is a cap
in the uploader, not a protocol limit. If it can be raised, a larger page
becomes possible.

A fuller 23KB version with a marquee, animated furnace, thoughts terminal
and FAQ was built and reverted at this cap. It is not in the tree, but it
is in git history if the ceiling ever lifts.

## Constraints

No external dependencies: inline `<style>`, inline `<script>`, no image
files, system fonts only. The only outbound URLs are hyperlinks (pools.fun,
bankr.bot, opensea.io).

The sprite is drawn to a `<canvas>` from a text grid rather than embedded
as a Base64 image — far cheaper, and sharp at any size. The page contains
no 4-byte characters.

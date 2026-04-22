# heuristics

every rule has an id, a description, a positive fixture, and a negative fixture.
ids are referenced from `event.notes` so users can trace what fired. new rules
must ship with both fixtures or they do not get merged.

## SAND-01: classic sandwich

three swaps on the same pool: a front-run by a searcher, a victim swap, a
back-run by the same searcher. front and back run in opposite directions.

requirements:

- `front.pool == victim.pool == back.pool`
- `front.sender == back.sender != victim.sender`
- `front.token_in == victim.token_in` and `front.token_out == victim.token_out`
- `back.token_in == victim.token_out` and `back.token_out == victim.token_in`
- `front.tx_index < victim.tx_index < back.tx_index`

scoring: base 0.70. coinbase-transfer raises by 0.10. presence of a victim
record raises by 0.05.

shipped in: v0.1.

## BACK-01: one-step backrun

two consecutive swaps on the same pool by different senders, same direction.
the second swap is treated as an arb candidate against the first.

requirements:

- `a.pool == b.pool`
- `a.sender != b.sender`
- `a.token_in == b.token_in` and `a.token_out == b.token_out`
- `a.tx_index + 1 == b.tx_index`

scoring: base 0.50. coinbase-transfer raises by 0.10.

shipped in: v0.1.

## JIT-01: just-in-time liquidity

uniswap v3 only. a position is opened (mint) and closed (burn) in the same
block, surrounding a victim swap. the searcher captures fees from the victim
and rebalances out before the block ends.

planned for v0.2.

## ARB-01: atomic multi-hop arb

a single transaction touches three or more pools and ends with a profit
denominated in the input token. typical on stable triangles
(weth → usdc → wbtc → weth).

planned for v0.2.

## LIQ-01: liquidation w/ priority manipulation

aave or compound liquidation where the searcher front-runs the
`liquidationCall` with a price-impact swap that pushes the victim past
threshold.

planned for v0.3.

## ORACLE-01: oracle-update sandwich

similar to SAND-01 but the victim is an oracle-update transaction. the
searcher positions before the update lands and exits after.

planned for v0.3.

## why each rule has a numbered id

users get a verdict; auditors need a reason. quoting a rule id in a forum
post or a postmortem is more useful than re-explaining the heuristic each time.

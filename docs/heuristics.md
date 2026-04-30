# heuristics

every rule has an id, a description, a positive fixture, and a negative fixture.
ids are referenced from `event.notes` so users can trace what fired. new rules
must ship with both fixtures or they do not get merged.

## SAND-01: classic sandwich

three swaps on the same pool inside one slot: a front-run by a searcher,
a victim swap, a back-run by the same searcher. front and back run in
opposite directions.

requirements:

- `front.pool == victim.pool == back.pool`
- `front.sender == back.sender != victim.sender`
- `front.token_in == victim.token_in` and `front.token_out == victim.token_out`
- `back.token_in == victim.token_out` and `back.token_out == victim.token_in`
- `front.tx_index < victim.tx_index < back.tx_index`

scoring: base 0.70. jito-tip raises by 0.10. presence of a victim record
raises by 0.05.

shipped in: v0.2.

## BACK-01: one-step backrun

two consecutive swaps on the same pool by different senders, same direction.
the second swap is treated as an arb candidate against the first.

requirements:

- `a.pool == b.pool`
- `a.sender != b.sender`
- `a.token_in == b.token_in` and `a.token_out == b.token_out`
- `a.tx_index + 1 == b.tx_index`

scoring: base 0.50. jito-tip raises by 0.10.

shipped in: v0.2.

## JIT-01: just-in-time liquidity

orca whirlpool concentrated-liquidity only. a position is opened (mint)
and closed (burn) inside the same slot, surrounding a victim swap. the
searcher captures fees from the victim and rebalances out before the
slot ends.

planned for v0.3.

## ARB-01: atomic multi-hop arb

a single signature touches three or more pools and ends with a profit
denominated in the input mint. typical on stable triangles
(sol → usdc → usdt → sol).

planned for v0.3.

## LEAD-01: leader collusion

the same validator (leader) catches multiple jito bundles inside N
consecutive slots from the same searcher. statistically anomalous —
suggests a relationship between the leader and the searcher that
side-steps the public jito auction.

planned for v0.4.

## LIQ-01: liquidation w/ priority manipulation

kamino or marginfi liquidation where the searcher front-runs the
liquidation instruction with a price-impact swap that pushes the
victim past threshold.

planned for v0.4.

## ORACLE-01: oracle-update sandwich (parked)

pyth / switchboard update sandwiches were on the eth-era roadmap.
solana oracle-update mechanics differ enough that the rule needs a
fresh design before it gets numbered. parked for now.

## why each rule has a numbered id

users get a verdict; auditors need a reason. quoting a rule id in a
forum post or a postmortem is more useful than re-explaining the
heuristic each time.

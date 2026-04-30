# roadmap

ships in order. each version closes the door on the previous one. nothing is "soon". if it is not in the repo it does not exist.

## v0.1 - archived (ethereum era)

shipped 2026-04-25 as an ethereum mev forensics agent. 0.1.0 + 0.1.1 are the
last ethereum-side tags. the v0.1.x branch is no longer maintained. fork it
under MIT if you want to keep the ethereum line alive.

## v0.2 - shipped 2026-04-30 (chain pivot to solana)

- raydium amm v4 + orca whirlpool inner-instruction decoders
- SAND-01 sandwich rule on solana pools
- BACK-01 backrun rule on solana pools
- jito tip detection across the eight canonical tip accounts
- validator (leader) attribution table
- core types reshaped for slot / signature / lamports / compute units
- rust crate refactored for solana semantics
- demo + cli running against a synthetic raydium sandwich fixture
- ci green on python 3.9 to 3.12 and rust stable

## v0.3 - in flight

- wire `ingest-rs` via pyo3 so geyser / shredstream live ingest actually runs
- JIT-01 just-in-time liquidity rule for orca whirlpool concentrated positions
- ARB-01 atomic multi-hop arb rule (3+ pools in a single signature)
- fixture replay command (`hikara demo replay <slot>`) loading from `tests/fixtures/slots/`
- structured cli output mode (`--format json`)

## v0.4 - planned

- meteora dlmm + meteora amm + lifinity v2 decoders
- LEAD-01 leader collusion rule (same validator catches multiple bundles in N consecutive slots)
- LIQ-01 kamino + marginfi liquidation rule
- per-searcher pnl leaderboard
- per-leader bundle share dashboard

## v0.5 - planned

- weekly digest job emitting jsonl rollup
- prometheus output sink
- slack + discord output sinks
- jupiter v6 swap-route flattening (so jupiter-routed victims are correctly attributed back to the underlying pool)

## v0.6 - speculative

- jito-shredstream-proxy low-latency mode (sub-leader-level visibility)
- pump.fun bonded swap decoder
- phoenix clob decoder
- raydium clmm decoder
- pyo3 wheels published for linux + macos + windows

## not on the roadmap

we do not plan to add:

- a wallet, signer, or executor
- bundle submission
- a paid api
- a frontend that hides the data
- closed-source detection logic

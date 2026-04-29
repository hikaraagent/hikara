# roadmap

ships in order. each version closes the door on the previous one. nothing is "soon". if it is not in the repo it does not exist.

## v0.1 - shipped 2026-04-25

- sandwich + backrun rules
- uniswap v2 + v3 decode
- demo + cli + offline fixtures
- ci green on python 3.9, 3.10, 3.11, 3.12 and rust stable

## v0.2 - in flight

<!-- mempool ingest moves into the rust crate via pyo3. python keeps the api stable. -->

- wire `ingest-rs` via pyo3 so live mempool actually runs
- jit liquidity heuristic (JIT-01)
- atomic multi-hop arb heuristic (ARB-01)
- fixture replay command (`hakiri demo replay <id>`) loading from `tests/fixtures/blocks/`
- structured cli output mode (`--format json`)

## v0.3 - planned

- aave + compound liquidation rule (LIQ-01)
- oracle-update sandwich rule (ORACLE-01)
- balancer v2 + curve decoders
- base + arbitrum support
- per-searcher pnl leaderboard

## v0.4 - planned

- per-builder coinbase share dashboard
- weekly digest job emitting jsonl rollup
- prometheus output sink
- slack + discord output sinks

## v0.5 - speculative

- reth `mev` namespace integration when stable
- local low-latency node mode
- pyo3 wheels published for linux + macos + windows

## not on the roadmap

we do not plan to add:

- a wallet, signer, or executor
- bundle submission
- a paid api
- a frontend
- token-related logic of any kind

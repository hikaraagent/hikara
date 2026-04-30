# changelog

all notable changes ship here. format follows [keep a changelog](https://keepachangelog.com).

## [0.2.0] - 2026-04-30 — chain pivot to solana

this is a scope change. the v0.1.x line was an ethereum mev forensics agent.
v0.2.0 moves the entire detector to **solana**. nothing about the brand,
domain, or contributor zones changed. only the chain and the dex stack.

if you starred this repo for ethereum-side mev, that work lives at the
**v0.1.1 tag** and the codebase before this commit. fork it under MIT —
no need to ask. ongoing development is solana-only from here.

### added
- raydium amm v4 inner-instruction swap decoder
- orca whirlpool inner-instruction swap decoder
- known solana program-id table (raydium clmm, meteora dlmm, lifinity, jupiter v4/v6, pump.fun, jito tip)
- jito tip detector with the eight canonical tip accounts
- validator (leader) attribution table, seeded with public high-stake validators
- solana mev searcher label table, seeded with placeholder evidence
- ingest stubs for yellowstone-grpc geyser and jito-shredstream-proxy
- jito block engine bundle reader stub
- core types now carry `slot`, `signature`, `compute_unit_price`, `compute_units`, `jito_tip_lamports`
- new `classify_slot()` entry point alongside the legacy `classify_block` alias

### changed
- pyproject deps: dropped `eth-utils`, `eth-abi`, `eth-hash[pycryptodome]`. added `based58`.
- `Bundle.builder` field renamed `Bundle.leader` (validator pubkey, not block builder)
- `Event.coinbase_transfer_wei` renamed `Event.jito_tip_lamports`
- `Victim.realized_loss_wei` renamed `Victim.realized_loss_lamports`
- `SwapTx.tx_hash` renamed `SwapTx.signature`; `block_number` renamed `slot`
- `Event.profit_wei` renamed `Event.profit_lamports`; `profit_eth` property renamed `profit_sol`
- env vars: `HAKIRI_HTTP_URL` → `HAKIRI_RPC_HTTP_URL`. `HAKIRI_WS_URL` → `HAKIRI_RPC_WS_URL`. `HAKIRI_RELAY_URLS` → `HAKIRI_JITO_BLOCK_ENGINE_URL`. `HAKIRI_BACKFILL_BLOCKS` → `HAKIRI_BACKFILL_SLOTS`.
- trace mode values: `debug`/`parity`/`rpc` → `getblock`/`geyser`/`shredstream`
- rust crate: `SwapLeg.tx_hash` → `signature`. `Bundle.block_number` → `slot`. `coinbase_transfer_wei` → `jito_tip_lamports`. `PendingTx` aliased to `StreamedTx` for backward-compat.
- demo fixture moved from a uniswap v3 sandwich on weth/usdc to a raydium amm v4 sandwich on sol/usdc
- readme, roadmap, architecture, heuristics, glossary fully rewritten

### removed
- `src/hakiri/decode/uniswap_v2.py`, `uniswap_v3.py`, `routers.py`
- `src/hakiri/enrich/builder.py` (PBS-style block builders)
- `src/hakiri/enrich/coinbase.py` (coinbase-transfer detection on eth)
- `src/hakiri/ingest/mempool.py`, `builder.py` (eth pending-tx + relay stubs)
- ethereum-specific topics, keywords, and classifier metadata

### honest status

what is **not** shipped in 0.2.0:

- the geyser / shredstream live ingest is still a stub. `hakiri scan` falls through to demo when called.
- jit, atomic-arb, leader-collusion, liquidation rules are planned for v0.3 / v0.4.
- meteora, lifinity, pump.fun, phoenix, raydium-clmm decoders are stubs.
- the searcher and leader tables are seeded with placeholders. real curation lands as PRs from the community.
- the ai filter is still a no-op pass-through.

read-only by design. no wallet, no signer, no executor. the chain changed; the philosophy did not.

## [0.1.1] - 2026-04-30 — last ethereum-era release

### added
- top-level `--version` / `-V` flag on the cli for fast version checks
- banner asset at `assets/bannerhakiri.jpg` referenced from the readme
- twitter, telegram, and website badges on the readme

### changed
- project homepage now points to https://hakiri.xyz/ (pyproject + repo metadata)
- ascii wordmark dropped from readme; the banner already shows it

### fixed
- ruff import order in `enrich/searcher.py` and `enrich/builder.py`
- duplicate `authors` / `description` / `license` keys in `ingest-rs/Cargo.toml`

## [0.1.0] - 2026-04-25 — first public release (ethereum)

### added
- core types: `Event`, `Bundle`, `SwapTx`, `Victim`, `Verdict`
- sandwich detector (SAND-01) and one-step backrun detector (BACK-01) on uniswap v2/v3
- uniswap v2 + v3 swap log decoders
- known-router, known-builder, known-searcher lookup tables
- coinbase-transfer detector for bundle attribution
- rule-based scorer with confidence cap at 0.95
- output sinks: stdout (rich), jsonl, webhook (httpx)
- typer cli with `scan`, `investigate`, `demo`, `version` subcommands
- offline `demo scan` and `demo investigate` driving synthetic fixtures
- pydantic-settings config loader with env-var prefix `HAKIRI_`
- rust crate `hakiri-ingest`: pending-tx types, sandwich classifier, trace types
- ci workflow on push and pr: python matrix (3.9 - 3.12) + rust stable

[unreleased]: https://github.com/hakiriagent/hakiri/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/hakiriagent/hakiri/releases/tag/v0.2.0
[0.1.1]: https://github.com/hakiriagent/hakiri/releases/tag/v0.1.1
[0.1.0]: https://github.com/hakiriagent/hakiri/releases/tag/v0.1.0

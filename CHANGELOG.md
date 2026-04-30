# changelog

all notable changes ship here. format follows [keep a changelog](https://keepachangelog.com).

## [0.3.0] - 2026-04-30 — rebrand: hakiri → hikara

this is a rebrand. the project was published as **hakiri** for two days
(v0.1.0 ethereum, v0.2.0 solana pivot). it ships from v0.3.0 onward as
**hikara**. brand, name, package, cli command, env-var prefix, banner,
domain — all changed. nothing else.

if you installed v0.2.0 — uninstall and reinstall under the new name.

### changed

- python package: `hakiri` → `hikara`. import path is `from hikara import ...`
- cli command: `hakiri` → `hikara`. add `hikara --version` to verify
- pyproject: `name = "hakiri"` → `"hikara"`. console script entrypoint renamed
- rust crate: `hakiri-ingest` → `hikara-ingest`. lib name `hikara_ingest`
- env-var prefix: `HAKIRI_*` → `HIKARA_*`. all keys renamed in lockstep
- banner asset: `assets/bannerhakiri.jpg` → `assets/bannerhikara.jpg`
- repo description and topics on github
- domain: hakiri.xyz → hikara.xyz (both retained for redirect during transition)

### kept

- github repo url stays `hikaraagent/hikara` (account login unchanged, slug renamed)
- maintainer handles unchanged: hakiri (lead), 0xnova, mikrohash, luka
- contributor zones in CODEOWNERS unchanged in scope, only paths updated
- twitter @HakiriAgent stays active during transition; new @HikaraAgent will be set as the canonical handle when ready
- license, philosophy, heuristic ids (SAND-01, BACK-01, ...), confidence cap (0.95)

### removed

- nothing functional. the rename is brand-only. all detection logic, decoders,
  scoring, and ingest stubs from v0.2.0 carry forward identically.

### honest status

what is **not** shipped in 0.3.0:

- still no live geyser ingest (planned for next minor)
- still placeholder seed data in searcher / leader tables
- still a no-op ai filter
- the v0.1.x and v0.2.0 historical names appear in earlier changelog
  entries below. those names were the actual brand at that time.

read-only by design. no wallet, no signer, no executor. the brand changed; the philosophy did not.

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
- env vars: `HIKARA_HTTP_URL` → `HIKARA_RPC_HTTP_URL`. `HIKARA_WS_URL` → `HIKARA_RPC_WS_URL`. `HIKARA_RELAY_URLS` → `HIKARA_JITO_BLOCK_ENGINE_URL`. `HIKARA_BACKFILL_BLOCKS` → `HIKARA_BACKFILL_SLOTS`.
- trace mode values: `debug`/`parity`/`rpc` → `getblock`/`geyser`/`shredstream`
- rust crate: `SwapLeg.tx_hash` → `signature`. `Bundle.block_number` → `slot`. `coinbase_transfer_wei` → `jito_tip_lamports`. `PendingTx` aliased to `StreamedTx` for backward-compat.
- demo fixture moved from a uniswap v3 sandwich on weth/usdc to a raydium amm v4 sandwich on sol/usdc
- readme, roadmap, architecture, heuristics, glossary fully rewritten

### removed
- `src/hikara/decode/uniswap_v2.py`, `uniswap_v3.py`, `routers.py`
- `src/hikara/enrich/builder.py` (PBS-style block builders)
- `src/hikara/enrich/coinbase.py` (coinbase-transfer detection on eth)
- `src/hikara/ingest/mempool.py`, `builder.py` (eth pending-tx + relay stubs)
- ethereum-specific topics, keywords, and classifier metadata

### honest status

what is **not** shipped in 0.2.0:

- the geyser / shredstream live ingest is still a stub. `hikara scan` falls through to demo when called.
- jit, atomic-arb, leader-collusion, liquidation rules are planned for v0.3 / v0.4.
- meteora, lifinity, pump.fun, phoenix, raydium-clmm decoders are stubs.
- the searcher and leader tables are seeded with placeholders. real curation lands as PRs from the community.
- the ai filter is still a no-op pass-through.

read-only by design. no wallet, no signer, no executor. the chain changed; the philosophy did not.

## [0.1.1] - 2026-04-30 — last ethereum-era release

### added
- top-level `--version` / `-V` flag on the cli for fast version checks
- banner asset at `assets/bannerhikara.jpg` referenced from the readme
- twitter, telegram, and website badges on the readme

### changed
- project homepage now points to https://hikara.xyz/ (pyproject + repo metadata)
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
- pydantic-settings config loader with env-var prefix `HIKARA_`
- rust crate `hikara-ingest`: pending-tx types, sandwich classifier, trace types
- ci workflow on push and pr: python matrix (3.9 - 3.12) + rust stable

[unreleased]: https://github.com/hikaraagent/hikara/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/hikaraagent/hikara/releases/tag/v0.3.0
[0.2.0]: https://github.com/hikaraagent/hikara/releases/tag/v0.2.0
[0.1.1]: https://github.com/hikaraagent/hikara/releases/tag/v0.1.1
[0.1.0]: https://github.com/hikaraagent/hikara/releases/tag/v0.1.0

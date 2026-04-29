# changelog

all notable changes ship here. format follows [keep a changelog](https://keepachangelog.com).

## [0.1.1] - 2026-04-30

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

### honest status

still a v0.1.x patch. live mempool ingest is the v0.2 work. no new heuristics shipped in this release.

## [unreleased]

### added
- jit liquidity heuristic (JIT-01) prototype, behind a feature flag
- balancer v2 vault decoder skeleton

### changed
- cli `scan` now falls back to demo when no rpc is configured

### fixed
- v3 decoder no longer crashes on positive amount0 + positive amount1 logs (malformed pool)

## [0.1.0] - 2026-04-25

### added
- core types: `Event`, `Bundle`, `SwapTx`, `Victim`, `Verdict`
- sandwich detector (SAND-01) and one-step backrun detector (BACK-01)
- uniswap v2 swap log decoder
- uniswap v3 swap log decoder
- known-router and known-builder lookup tables
- known-searcher lookup table
- coinbase-transfer detector for bundle attribution
- rule-based scorer with confidence cap at 0.95
- output sinks: stdout (rich), jsonl, webhook (httpx)
- typer cli with `scan`, `investigate`, `demo`, `version` subcommands
- offline `demo scan` and `demo investigate` driving synthetic fixtures
- pydantic-settings config loader with env-var prefix `HAKIRI_`
- rust crate `hakiri-ingest`: pending-tx types, sandwich classifier, trace types
- pytest suite covering classifier, scorer, decoder, output, demo, config
- cargo integration tests covering the rust sandwich classifier
- ci workflow on push and pr: python matrix (3.9 - 3.12) + rust stable
- ruff, cargo fmt, cargo clippy with `-D warnings` enforced
- pre-commit hooks for ruff and cargo fmt
- issue templates: bug, feature, new searcher
- pull request template
- codeowners mapping zones to handles
- dependabot config for pip and cargo
- stale workflow auto-closing inactive issues after 60 days
- labeler workflow auto-tagging prs by path

### honest status

what's not done in 0.1.0:

- live mempool subscribe is a stub. `hakiri scan` falls through to demo when called.
- jit, atomic-arb, liquidation, oracle rules are planned, not shipped
- only ethereum mainnet. l2s land in v0.3
- ai filter is a noop pass-through. enabling `ANTHROPIC_API_KEY` does not change scoring yet
- balancer and curve decoders are stubs

read-only by design. no wallet, no signer, no executor.

[unreleased]: https://github.com/hakiriagent/hakiri/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/hakiriagent/hakiri/releases/tag/v0.1.1
[0.1.0]: https://github.com/hakiriagent/hakiri/releases/tag/v0.1.0

<div align="center">

<img src="assets/bannerhikara.jpg" alt="hikara" width="100%" />

### solana mev forensics agent

read-only by design. shows what got taken from you in the dark.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)
[![Rust](https://img.shields.io/badge/rust-stable-orange.svg)](ingest-rs/Cargo.toml)
[![CI](https://img.shields.io/badge/ci-pytest%20%2B%20cargo-success.svg)](.github/workflows/ci.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![X / Twitter](https://img.shields.io/badge/x-@HikaraAgent-000000.svg)](https://x.com/HikaraAgent)
[![Website](https://img.shields.io/badge/site-hikara.xyz-white.svg)](https://hikara.xyz/)

[![Solana](https://img.shields.io/badge/chain-solana-9945FF.svg)]()
[![Raydium](https://img.shields.io/badge/decode-raydium%20%2B%20orca-14F195.svg)]()
[![Jito](https://img.shields.io/badge/attribution-jito%20bundles-000000.svg)]()

---

[**what it does**](#what-it-does) ·
[**how it works**](#how-it-works) ·
[**heuristics**](#detection-heuristics) ·
[**quickstart**](#quickstart) ·
[**cli**](#cli-reference) ·
[**architecture**](#architecture) ·
[**roadmap**](#roadmap)

</div>

---

## what it does

- watches every slot on solana mainnet, decodes raydium and orca swaps, reconstructs jito bundles
- classifies the events: sandwich, jit, backrun, liquidation, atomic arb
- attributes leaders (validators), known searchers, and jito tip transfers
- emits a verdict per event with a confidence in [0.0, 0.95]. detector, not oracle

no wallet. no signer. no executor. no trading. anyone forking to build a sniper does so in their own repo.

## how it works

```
   geyser / shredstream             finalized slots
          │                                  │
          ▼                                  ▼
    ┌──────────────┐                  ┌──────────────┐
    │ ingest-rs    │                  │ getBlock     │
    │ grpc stream  │                  │ getTransaction│
    └──────┬───────┘                  └──────┬───────┘
           │                                 │
           └──────────────┬──────────────────┘
                          ▼
                  ┌───────────────┐
                  │ decode        │   raydium amm v4, orca whirlpool, jupiter routes
                  └──────┬────────┘
                         ▼
                  ┌──────────────┐
                  │ classify     │   SAND-01, BACK-01, JIT-01, ARB-01
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │ score        │   rule-based, capped at 0.95
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │ ai filter    │   optional. only reviews edge cases
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │ output sinks │   stdout · jsonl · webhook
                  └──────────────┘
```

every step is independent. you can plug in your own ingest, your own classifier, your own sink. the contract between layers is the `Event` dataclass in `src/hikara/core/types.py`.

## supported

| target                | status |
|-----------------------|:------:|
| solana mainnet        |   🟢   |
| raydium amm v4        |   🟢   |
| orca whirlpool        |   🟢   |
| jito bundle attribution |  🟢   |
| validator (leader) labels |  🟢  |
| meteora dlmm          |   🟡   |
| meteora amm           |   🟡   |
| lifinity v2           |   🟡   |
| jupiter v6 routes     |   🟡   |
| pump.fun bonded swaps |   ⚪   |
| raydium clmm          |   ⚪   |
| phoenix clob          |   ⚪   |

🟢 primary · 🟡 ready, low coverage · ⚪ stub or planned

## detection heuristics

each rule has an id used in `event.notes` so you can trace what fired.

| id        | what it catches                                                | shipped in |
|-----------|----------------------------------------------------------------|:----------:|
| SAND-01   | classic sandwich: front + victim + back same pool, opp dirs    |   v0.2     |
| BACK-01   | one-step backrun arb against a user swap                       |   v0.2     |
| JIT-01    | just-in-time liquidity add+remove around a victim swap         |   v0.3     |
| ARB-01    | atomic multi-hop arb across 3+ pools in a single tx            |   v0.3     |
| LEAD-01   | leader collusion: same leader catches multiple bundles in N consecutive slots | v0.4 |
| LIQ-01    | kamino/marginfi liquidation w/ priority manipulation           |   v0.4     |

new rules ship behind a version, not a feature flag. the repo is the source of truth.

## quickstart

requires python 3.9+ and rust stable.

```sh
git clone https://github.com/hakiriagent/hikara.git
cd hikara

# install python package + dev deps
make install

# build the rust ingest crate
cd ingest-rs && cargo build --release && cd ..

# run an offline demo (zero network)
hikara demo investigate

# run the live scanner against your rpc
cp .env.example .env
$EDITOR .env   # set HIKARA_RPC_HTTP_URL and / or HIKARA_GEYSER_GRPC_URL
hikara scan
```

no rpc? `hikara demo scan` shows the full pipeline against synthetic fixtures.

## cli reference

```sh
hikara --version                  # quick version check
hikara version                    # version + active config
hikara scan                       # live slot + bundle scan
hikara scan --once                # one slot then exit (smoke test)
hikara investigate <sig|slot>     # walk the pipeline on a specific target

hikara demo scan                  # canned scan against a synthetic slot
hikara demo investigate           # full pipeline trace, prints every step
hikara demo replay <id>           # replay a recorded fixture
```

example output for `hikara demo investigate`:

```
─────────────────── step 1. decoded swaps ────────────────────
  slot 287000000 idx 0  sender JTOArByrMv...  pool 58oQChx4yW...  in 8_000_000_000  out 24_000_000_000
  slot 287000000 idx 1  sender VicT1mw411...  pool 58oQChx4yW...  in 2_000_000_000  out 5_950_000_000
  slot 287000000 idx 2  sender JTOArByrMv...  pool 58oQChx4yW...  in 24_500_000_000  out 8_300_000_000

─────────────────── step 2. classifier rules ─────────────────
  rules fired: ['SAND-01']
  slot verdict: likely
  events found:  1

─────────────────── step 3. score per event ─────────────────
  sandwich slot 287000000
    base[sandwich]=0.70
    jito_tip>0:+0.10
    bundle.txs>=2:+0.05
    victims_present:+0.05
    -> verdict=confirmed conf=0.900
─────────────────────── done ────────────────────────────────
```

## architecture

```
hikara/
├── src/hikara/                    python package
│   ├── core/                      types · classify · score
│   ├── decode/                    raydium · orca · program ids
│   ├── enrich/                    leader · jito tip · searcher
│   ├── ingest/                    geyser + jito relay stubs (rust later)
│   ├── output/                    stdout · jsonl · webhook
│   ├── ai/                        optional rule reviewer
│   ├── demo/                      offline scripted demos
│   └── cli.py                     typer entrypoint
├── ingest-rs/                     low-level ingest crate (rust)
│   └── src/ {mempool,bundle,trace}.rs
├── tests/                         pytest suite
└── docs/                          architecture · heuristics · glossary
```

| zone                    | language | maintainer    |
|-------------------------|----------|---------------|
| core, scoring, ci       | python   | @hakiriagent  |
| ingest-rs, geyser       | rust     | @0xnova       |
| classify, heuristics    | python   | @mikrohash    |
| decode, output, cli     | python   | @luka         |

## roadmap

| version | scope                                                                        | status  |
|---------|------------------------------------------------------------------------------|:-------:|
| v0.1    | (eth-era) sandwich + backrun on uniswap v2/v3. archived, see CHANGELOG.       | archived |
| v0.2    | chain pivot to solana. raydium + orca decode. SAND-01 + BACK-01 on sol. demo + cli. | shipped |
| v0.3    | rust geyser ingest wired via pyo3. JIT-01 + ARB-01 rules. fixture replay.     | now     |
| v0.4    | meteora + lifinity decoders. LEAD-01 leader collusion. LIQ-01 liquidation.    | planned |
| v0.5    | per-searcher pnl leaderboard. per-leader bundle share. weekly digest.        | planned |
| v0.6    | shredstream low-latency mode. pump.fun + phoenix decoders.                    | planned |

## contributing

short version: ship code that passes ci, write a clear pr description, no llm-generated readmes.

new searchers, leaders, and program ids are the easiest path in. open a PR against `src/hikara/enrich/searcher.py`, `src/hikara/enrich/leader.py`, or `src/hikara/decode/programs.py` with on-chain evidence (three signatures + slot numbers) in the description.

read [CONTRIBUTING.md](CONTRIBUTING.md) for the full guidelines.

## license

[MIT](LICENSE). use it, fork it, ship better.

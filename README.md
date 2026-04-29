<div align="center">

<img src="assets/bannerhakiri.jpg" alt="hakiri" width="100%" />

```
            ██╗  ██╗ █████╗ ██╗  ██╗██╗██████╗ ██╗
            ██║  ██║██╔══██╗██║ ██╔╝██║██╔══██╗██║
            ███████║███████║█████╔╝ ██║██████╔╝██║
            ██╔══██║██╔══██║██╔═██╗ ██║██╔══██╗██║
            ██║  ██║██║  ██║██║  ██╗██║██║  ██║██║
            ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝
```

### ethereum mev forensics agent

read-only by design. shows what got taken from you in the dark.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)
[![Rust](https://img.shields.io/badge/rust-stable-orange.svg)](ingest-rs/Cargo.toml)
[![CI](https://img.shields.io/badge/ci-pytest%20%2B%20cargo-success.svg)](.github/workflows/ci.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[![Ethereum](https://img.shields.io/badge/chain-ethereum-627EEA.svg)]()
[![viem](https://img.shields.io/badge/decode-uniswap%20v2%2Fv3-ff007a.svg)]()
[![Flashbots](https://img.shields.io/badge/relays-flashbots%20%2B%20ultrasound-black.svg)]()

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

- watches every block on ethereum mainnet, decodes the swap logs, reconstructs bundles
- classifies the events: sandwich, jit, backrun, liquidation, atomic arb
- attributes builders (beaverbuild, titan, flashbots, rsync, builder0x69) and known searchers
- emits a verdict per event with a confidence in [0.0, 0.95]. detector, not oracle

no wallet. no signer. no executor. no trading. anyone forking to build a sniper does so in their own repo.

## how it works

```
   pending mempool                  finalized blocks
        │                                  │
        ▼                                  ▼
  ┌──────────────┐                  ┌──────────────┐
  │ ingest-rs    │                  │ trace_block  │
  │ ws subscribe │                  │ debug_trace  │
  └──────┬───────┘                  └──────┬───────┘
         │                                 │
         └──────────────┬──────────────────┘
                        ▼
                ┌───────────────┐
                │ decode  v2/v3 │   uniswap, sushi, balancer pools
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

every step is independent. you can plug in your own ingest, your own classifier, your own sink. the contract between layers is the `Event` dataclass in `src/hakiri/core/types.py`.

## supported

| target                | status |
|-----------------------|:------:|
| ethereum mainnet      |   🟢   |
| uniswap v2 swap logs  |   🟢   |
| uniswap v3 swap logs  |   🟢   |
| sushiswap v2 (alias)  |   🟢   |
| flashbots relay       |   🟢   |
| ultrasound relay      |   🟢   |
| balancer v2 vault     |   🟡   |
| curve pools           |   🟡   |
| L2: base, arbitrum    |   ⚪   |
| reth `mev` namespace  |   ⚪   |

🟢 primary · 🟡 ready, low coverage · ⚪ stub or planned

## detection heuristics

each rule has an id used in `event.notes` so you can trace what fired.

| id        | what it catches                                                | shipped in |
|-----------|----------------------------------------------------------------|:----------:|
| SAND-01   | classic sandwich: front + victim + back same pool, opp dirs    |   v0.1     |
| BACK-01   | one-step backrun arb against a user swap                       |   v0.1     |
| JIT-01    | just-in-time liquidity add+remove around a victim swap         |   v0.2     |
| ARB-01    | atomic multi-hop arb across 3+ pools in a single tx            |   v0.2     |
| LIQ-01    | aave/compound liquidation w/ priority manipulation             |   v0.3     |
| ORACLE-01 | sandwich-style prep around oracle update tx                    |   v0.3     |

new rules ship behind a version, not a feature flag. the repo is the source of truth.

## quickstart

<!-- read-only by design. no wallet, no signer, no executor. -->

requires python 3.9+ and rust stable.

```sh
git clone https://github.com/hakiriagent/hakiri.git
cd hakiri

# install python package + dev deps
make install

# build the rust ingest crate
cd ingest-rs && cargo build --release && cd ..

# run an offline demo (zero network)
hakiri demo investigate

# run the live scanner against your rpc
cp .env.example .env
$EDITOR .env   # set HAKIRI_WS_URL or HAKIRI_HTTP_URL
hakiri scan
```

no rpc? `hakiri demo scan` shows the full pipeline against synthetic fixtures.

## cli reference

```sh
hakiri version                    # version + active config
hakiri scan                       # live mempool + block scan
hakiri scan --once                # one block then exit (smoke test)
hakiri investigate <tx|block>     # walk the pipeline on a specific target

hakiri demo scan                  # canned scan against a synthetic block
hakiri demo investigate           # full pipeline trace, prints every step
hakiri demo replay <id>           # replay a recorded fixture
```

example output for `hakiri demo investigate`:

```
─────────────────── step 1. decoded swaps ────────────────────
  block 21000000 idx 0  sender 0xa69BabE...  pool 0x88e6A0c2...  in 8000000000000000000  out 24000000000
  block 21000000 idx 1  sender 0xCAFE8888...  pool 0x88e6A0c2...  in 2000000000000000000  out 5950000000
  block 21000000 idx 2  sender 0xa69BabE...  pool 0x88e6A0c2...  in 24500000000  out 8300000000000000

─────────────────── step 2. classifier rules ─────────────────
  rules fired: ['SAND-01']
  block verdict: likely
  events found:  1

─────────────────── step 3. score per event ─────────────────
  sandwich block 21000000
    base[sandwich]=0.70
    coinbase_transfer>0:+0.10
    bundle.txs>=2:+0.05
    victims_present:+0.05
    -> verdict=confirmed conf=0.900
─────────────────────── done ────────────────────────────────
```

## architecture

```
hakiri/
├── src/hakiri/                    python package
│   ├── core/                      types · classify · score
│   ├── decode/                    uniswap v2/v3 + router labels
│   ├── enrich/                    builder · searcher · coinbase transfer
│   ├── ingest/                    rpc + mempool + trace stubs (rust later)
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
| ingest-rs, mempool      | rust     | @0xnova       |
| classify, heuristics    | python   | @mikrohash    |
| decode, output          | python   | @luka         |

## roadmap

| version | scope                                                                        | status  |
|---------|------------------------------------------------------------------------------|:-------:|
| v0.1    | sandwich + backrun rules. uniswap v2/v3 decode. demo + cli.                  | shipped |
| v0.2    | rust ingest wired via pyo3. jit + atomic arb rules. fixture replay.          | now     |
| v0.3    | liquidation + oracle rules. balancer + curve. base + arbitrum support.       | planned |
| v0.4    | per-searcher leaderboard. per-builder coinbase share. weekly digest.         | planned |
| v0.5    | reth `mev` namespace integration. low-latency local node mode.               | planned |

## contributing

short version: ship code that passes ci, write a clear pr description, no llm-generated readmes.

new searchers and builders are the easiest path in. open a PR against `src/hakiri/enrich/builder.py` or `src/hakiri/enrich/searcher.py` with on-chain evidence in the description.

read [CONTRIBUTING.md](CONTRIBUTING.md) for the full guidelines.

## license

[MIT](LICENSE). use it, fork it, ship better.


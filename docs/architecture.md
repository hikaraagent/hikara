# architecture

hakiri is intentionally a pipeline of small layers. you can replace any layer
without touching the others. the only stable contract is the `Event` type in
`src/hakiri/core/types.py`.

```
ingest  →  decode  →  classify  →  score  →  (ai filter)  →  sink
```

## ingest layer

two source families feed the pipeline:

1. **streaming** (sub-confirmation). yellowstone-grpc geyser subscription
   for account / tx / slot notifications, or jito-shredstream-proxy for
   sub-leader-level latency.
2. **finalized slots** (post-inclusion). `getBlock` with full transactions
   for canonical retrieval, `getTransaction` for per-signature enrichment.

the live ingest path runs in `ingest-rs/`. python has stubs at
`src/hakiri/ingest/{geyser,jito_relay,trace}.py` so the rest of the pipeline
can be exercised without a node.

## decode layer

parsed inner instructions are converted into `SwapTx` records. supported
programs:

- raydium amm v4 (`675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`)
- orca whirlpool (`whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc`)

meteora dlmm + amm, lifinity v2, raydium clmm, pump.fun, phoenix, and
jupiter v4/v6 are recognized in `decode/programs.py` for labeling but
their swap decoders are stubs.

## classify layer

pure functions over `SwapTx` lists ordered by `tx_index` (within a slot).
each rule has an id:

- `SAND-01` — classic sandwich
- `BACK-01` — one-step backrun arb

new rules ship with a fixture and a numbered id. ids appear in
`docs/heuristics.md` and on the event itself via `event.notes`.

## score layer

rule-based confidence in `[0.0, 0.95]`. capped on purpose. the breakdown is
returned to the caller so every confidence value is fully traceable. on
solana the strongest single bonus comes from a non-zero jito tip.

## ai filter layer

optional. only used when `ANTHROPIC_API_KEY` is set. the filter reviews
edge-case events and returns a minor adjustment, never an upgrade beyond
the cap. when disabled, the rule-based score is final.

## sink layer

three sinks ship in 0.2:

- `stdout` — rich-formatted terminal output
- `jsonl` — append-only file at the configured path
- `webhook` — POST to an arbitrary url, failures swallowed

`all` runs every configured sink. add your own by implementing an `emit`
method that takes `(event, score)`.

## why polyglot

mev forensics is bottlenecked by ingest latency. on solana that means
geyser / shredstream throughput. python is fast enough for classification
and scoring (a slot has tens to hundreds of swaps) but a poor fit for a
high-frequency grpc loop. rust handles the hot path; python handles the
analysis. they meet at the `Event` boundary.

# architecture

hakiri is intentionally a pipeline of small layers. you can replace any layer
without touching the others. the only stable contract is the `Event` type in
`src/hakiri/core/types.py`.

```
ingest  →  decode  →  classify  →  score  →  (ai filter)  →  sink
```

## ingest layer

two sources feed the pipeline:

1. **mempool** (pre-inclusion). a websocket subscription to pending transactions.
   used to detect bundles before they land.
2. **finalized blocks** (post-inclusion). either `eth_getLogs` (cheap, partial)
   or `debug_traceBlockByNumber` / `trace_block` (rich, expensive).

the live ingest path runs in `ingest-rs/`. python has stubs at
`src/hakiri/ingest/{mempool,builder,trace}.py` so the rest of the pipeline can
be exercised without a node.

## decode layer

receipts and logs are converted into `SwapTx` records. supported topics:

- uniswap v2 `Swap(address,uint256,uint256,uint256,uint256,address)`
- uniswap v3 `Swap(address,address,int256,int256,uint160,uint128,int24)`

balancer v2 and curve are stubs at this stage.

## classify layer

pure functions over `SwapTx` lists ordered by `tx_index`. each rule has an id:

- `SAND-01` — classic sandwich
- `BACK-01` — one-step backrun arb

new rules ship with a fixture and a numbered id. ids appear in
`docs/heuristics.md` and on the event itself via `event.notes`.

## score layer

rule-based confidence in `[0.0, 0.95]`. capped on purpose. the breakdown is
returned to the caller so every confidence value is fully traceable.

## ai filter layer

optional. only used when `ANTHROPIC_API_KEY` is set. the filter reviews
edge-case events and returns a minor adjustment, never an upgrade beyond
the cap. when disabled, the rule-based score is final.

## sink layer

three sinks ship in 0.1:

- `stdout` — rich-formatted terminal output
- `jsonl` — append-only file at the configured path
- `webhook` — POST to an arbitrary url, failures swallowed

`all` runs every configured sink. add your own by implementing an `emit`
method that takes `(event, score)`.

## why polyglot

mev forensics is bottlenecked by mempool latency. python is fast enough for
classification and scoring (a block is at most a few hundred logs) but a poor
fit for a high-frequency websocket loop. rust handles the hot path; python
handles the analysis. they meet at the `Event` boundary.

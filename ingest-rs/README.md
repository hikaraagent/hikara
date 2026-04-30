# hikara-ingest

low-level ingest crate for [hikara](https://github.com/hikaraagent/hikara).

handles the hot paths the python core defers:

- mempool websocket subscribe + decode
- bundle reconstruction from block traces
- relay payload polling

published as a rust library so the python package can call into it via
pyo3 in v0.2. for now it ships as a standalone binary used by the demo
fixtures.

## build

```sh
cargo build --release
cargo test --all-features
```

## layout

```
src/
  lib.rs       public api
  mempool.rs   pending-tx subscriber types
  bundle.rs    swap-leg classifier (sandwich, backrun)
  trace.rs    block trace types
tests/
  classify.rs  integration: sandwich pattern over fixture
```

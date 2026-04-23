# hakiri

ethereum mev forensics agent. read-only by design.

## what it does

- watches every block on ethereum mainnet
- decodes uniswap v2/v3 swap logs
- classifies sandwich and backrun events
- emits a verdict per event with a confidence in [0.0, 0.95]

no wallet. no signer. no trading.

## quickstart

```sh
make install
hakiri demo investigate
```

work in progress. see ROADMAP.md.

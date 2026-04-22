# glossary

domain terms used throughout hakiri.

**backrun** — an arbitrage transaction placed immediately after a known price-moving transaction.

**builder** — the entity that constructs a block. on ethereum mainnet under proposer-builder separation, the proposer (validator) outsources block-building to one of a small set of public builders.

**bundle** — an ordered group of transactions submitted together. searchers pay builders to include their bundle at a specific position.

**coinbase transfer** — an in-execution transfer of eth to `block.coinbase`. searchers use this to pay the builder for inclusion priority. presence and size are the strongest single signal that a transaction is part of an mev bundle.

**confidence cap** — hakiri scores never exceed 0.95. a detector, not an oracle.

**flashbots relay** — a public mev-boost relay forwarding builder bids to validators. one of several relays hakiri pulls payload data from.

**jit (just-in-time liquidity)** — adding liquidity to a pool, capturing fees from one specific incoming swap, and removing the liquidity in the same block.

**mempool** — the pool of transactions broadcast but not yet included. hakiri reads it to detect bundles before they land.

**pbs (proposer-builder separation)** — the post-merge ethereum architecture where validators receive bids from builders and choose the highest-paying block.

**relay** — a service relaying bids between builders and validators. flashbots, ultrasound, and titan are the most-used public relays.

**sandwich** — a front-run + back-run pair surrounding a victim swap on the same pool. the searcher buys before, sells after, captures the spread the victim creates.

**searcher** — a bot operator submitting bundles. mev-boost separates searchers from validators.

**tx_index** — the position of a transaction within its block. ordering matters for bundle reconstruction.

**verdict** — hakiri's human-readable label for a scored event: `confirmed` (≥0.85), `likely` (≥0.65), `suspected` (≥0.40), `noise` (<0.40).

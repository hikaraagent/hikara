# glossary

domain terms used throughout hikara.

**backrun** — an arbitrage transaction placed immediately after a known price-moving transaction in the same slot.

**bundle** — an ordered group of transactions submitted together. on solana, searchers send bundles to the jito block engine, which forwards them to leaders.

**confidence cap** — hikara scores never exceed 0.95. a detector, not an oracle.

**geyser** — solana's plugin interface for streaming account / slot / transaction notifications. yellowstone-grpc is the canonical implementation.

**inner instruction** — an instruction emitted by a program during execution of a top-level instruction (cross-program invocation). swap decoding on solana operates on inner instructions, not logs.

**jit (just-in-time liquidity)** — adding concentrated liquidity to a pool, capturing fees from one specific incoming swap, and removing the liquidity in the same slot. relevant on orca whirlpools.

**jito bundle** — a bundle submitted to the jito block engine. all-or-nothing inclusion. searchers pay validators via tip transfers to one of eight canonical tip accounts.

**jito tip** — a lamport transfer to one of the jito tip accounts inside a transaction. the strongest single signal that a tx is part of a jito bundle. presence and size are the bundle attribution heuristic.

**lamport** — the smallest unit of native sol. 1 sol = 1,000,000,000 lamports (1e9).

**leader** — the validator producing the current slot. one per slot, fixed by the leader schedule. on hikara, leaders are tagged via `Bundle.leader` and `Event.leader`.

**leader schedule** — the precomputed assignment of leaders to slots for an epoch. each slot has exactly one leader.

**pubkey** — a 32-byte ed25519 public key, base58 encoded. used for accounts, programs, and signers across solana.

**raydium amm v4** — solana's canonical constant-product amm. program id `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`.

**sandwich** — a front-run + back-run pair surrounding a victim swap on the same pool. the searcher buys before, sells after, captures the spread the victim creates.

**searcher** — a bot operator submitting bundles to the jito block engine. one searcher can use many wallets; hikara labels what is publicly attributable.

**shred** — a solana network packet carrying a fragment of a block. shredstream proxies allow listening to shreds before the block is fully assembled, giving sub-leader-level latency.

**signature** — the 64-byte ed25519 signature of a transaction. base58-encoded. unique per transaction; used as the identifier (replaces ethereum's tx_hash in hikara's data model).

**slot** — solana's unit of block time. one slot ≈ 400ms. each slot has a leader and may produce a block (slots can be skipped).

**tx_index** — the position of a transaction within its slot. ordering matters for bundle reconstruction.

**verdict** — hikara's human-readable label for a scored event: `confirmed` (≥0.85), `likely` (≥0.65), `suspected` (≥0.40), `noise` (<0.40).

**whirlpool** — orca's concentrated-liquidity amm. program id `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc`.

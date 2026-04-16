//! integration tests for the rust sandwich classifier. mirrors the python suite.

use hakiri_ingest::{classify_sandwich, SwapLeg};

fn weth() -> String {
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".to_string()
}
fn usdc() -> String {
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".to_string()
}
fn pool() -> String {
    "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640".to_string()
}

fn searcher() -> String {
    "0xa69BabEF1cA67A37Ffaf7a485DfFF3382056e78C".to_string()
}
fn victim() -> String {
    "0xCAFE8888888888888888888888888888888888AA".to_string()
}

fn leg(idx: u32, sender: String, token_in: String, token_out: String) -> SwapLeg {
    SwapLeg {
        tx_hash: format!("0x{:064x}", idx),
        tx_index: idx,
        sender,
        pool: pool(),
        token_in,
        token_out,
        amount_in: 1,
        amount_out: 1,
        coinbase_transfer_wei: 0,
        gas_used: 0,
    }
}

#[test]
fn detects_classic_sandwich() {
    let legs = vec![
        leg(0, searcher(), weth(), usdc()),
        leg(1, victim(), weth(), usdc()),
        leg(2, searcher(), usdc(), weth()),
    ];
    let result = classify_sandwich(&legs, 21_000_000);

    assert_eq!(result.bundles.len(), 1);
    assert_eq!(result.victim_hashes.len(), 1);
    assert!(result.rules.contains(&"SAND-01"));
    assert_eq!(result.bundles[0].searcher, searcher());
}

#[test]
fn ignores_non_sandwich_blocks() {
    let legs = vec![
        leg(0, searcher(), weth(), usdc()),
        leg(1, victim(), weth(), usdc()),
        leg(2, searcher(), weth(), usdc()),
    ];
    let result = classify_sandwich(&legs, 21_000_000);
    assert!(result.bundles.is_empty());
    assert!(result.rules.is_empty());
}

#[test]
fn requires_three_legs_minimum() {
    let legs = vec![
        leg(0, searcher(), weth(), usdc()),
        leg(1, victim(), weth(), usdc()),
    ];
    let result = classify_sandwich(&legs, 21_000_000);
    assert!(result.bundles.is_empty());
}

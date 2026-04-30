//! integration tests for the rust sandwich classifier. mirrors the python suite.

use hakiri_ingest::{classify_sandwich, SwapLeg};

fn sol() -> String {
    "So11111111111111111111111111111111111111112".to_string()
}
fn usdc() -> String {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v".to_string()
}
fn pool() -> String {
    "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2".to_string()
}

fn searcher() -> String {
    "JTOArByrMvDPfH8XgbQDbbYxWh5XEW1Bkau3jDXRcLg".to_string()
}
fn victim() -> String {
    "VicT1mw411111111111111111111111111111111111".to_string()
}

fn leg(idx: u32, sender: String, token_in: String, token_out: String) -> SwapLeg {
    SwapLeg {
        signature: format!("Sig{:061}", idx),
        tx_index: idx,
        sender,
        pool: pool(),
        token_in,
        token_out,
        amount_in: 1,
        amount_out: 1,
        jito_tip_lamports: 0,
        compute_units: 0,
    }
}

#[test]
fn detects_classic_sandwich() {
    let legs = vec![
        leg(0, searcher(), sol(), usdc()),
        leg(1, victim(), sol(), usdc()),
        leg(2, searcher(), usdc(), sol()),
    ];
    let result = classify_sandwich(&legs, 287_000_000);

    assert_eq!(result.bundles.len(), 1);
    assert_eq!(result.victim_signatures.len(), 1);
    assert!(result.rules.contains(&"SAND-01"));
    assert_eq!(result.bundles[0].searcher, searcher());
}

#[test]
fn ignores_non_sandwich_slots() {
    let legs = vec![
        leg(0, searcher(), sol(), usdc()),
        leg(1, victim(), sol(), usdc()),
        leg(2, searcher(), sol(), usdc()),
    ];
    let result = classify_sandwich(&legs, 287_000_000);
    assert!(result.bundles.is_empty());
    assert!(result.rules.is_empty());
}

#[test]
fn requires_three_legs_minimum() {
    let legs = vec![
        leg(0, searcher(), sol(), usdc()),
        leg(1, victim(), sol(), usdc()),
    ];
    let result = classify_sandwich(&legs, 287_000_000);
    assert!(result.bundles.is_empty());
}

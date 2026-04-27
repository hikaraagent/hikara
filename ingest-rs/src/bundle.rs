//! bundle reconstruction and classification.
//!
//! mirrors the python heuristic in `hakiri.core.classify` (SAND-01). the rust
//! implementation is here because once mempool ingest moves to rust
//! the classifier should run in the same process for latency.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SwapLeg {
    pub tx_hash: String,
    pub tx_index: u32,
    pub sender: String,
    pub pool: String,
    pub token_in: String,
    pub token_out: String,
    pub amount_in: u128,
    pub amount_out: u128,
    #[serde(default)]
    pub coinbase_transfer_wei: u128,
    #[serde(default)]
    pub gas_used: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Bundle {
    pub block_number: u64,
    pub searcher: String,
    pub legs: Vec<SwapLeg>,
    pub coinbase_transfer_wei: u128,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BundleClassification {
    pub bundles: Vec<Bundle>,
    pub victim_hashes: Vec<String>,
    pub rules: Vec<&'static str>,
}

/// detect sandwiches over an ordered slice of swap legs.
///
/// matches the python rule SAND-01: same pool, same searcher front+back,
/// opposite directions, with a third sender between them.
pub fn classify_sandwich(legs: &[SwapLeg], block_number: u64) -> BundleClassification {
    let mut legs: Vec<&SwapLeg> = legs.iter().collect();
    legs.sort_by_key(|l| l.tx_index);

    let mut bundles: Vec<Bundle> = Vec::new();
    let mut victims: Vec<String> = Vec::new();
    let mut used: Vec<usize> = Vec::new();

    let n = legs.len();
    if n < 3 {
        return BundleClassification {
            bundles,
            victim_hashes: victims,
            rules: vec![],
        };
    }

    'outer: for i in 0..n.saturating_sub(2) {
        if used.contains(&i) {
            continue;
        }
        for k in (i + 2)..n {
            if used.contains(&k) {
                continue;
            }
            for j in (i + 1)..k {
                if used.contains(&j) {
                    continue;
                }
                let (a, b, c) = (legs[i], legs[j], legs[k]);
                let same_pool = a.pool == b.pool && b.pool == c.pool;
                let same_searcher = a.sender == c.sender && a.sender != b.sender;
                let opp_dir = a.token_in == b.token_in
                    && a.token_out == b.token_out
                    && c.token_in == b.token_out
                    && c.token_out == b.token_in;

                if same_pool && same_searcher && opp_dir {
                    bundles.push(Bundle {
                        block_number,
                        searcher: a.sender.clone(),
                        legs: vec![a.clone(), c.clone()],
                        coinbase_transfer_wei: a.coinbase_transfer_wei + c.coinbase_transfer_wei,
                    });
                    victims.push(b.tx_hash.clone());
                    used.extend([i, j, k]);
                    continue 'outer;
                }
            }
        }
    }

    let rules = if bundles.is_empty() {
        vec![]
    } else {
        vec!["SAND-01"]
    };

    BundleClassification {
        bundles,
        victim_hashes: victims,
        rules,
    }
}

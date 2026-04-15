//! bundle reconstruction and classification (types only).

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

//! pending-tx subscriber types.
//!
//! the actual websocket loop lives in the binary target. this module
//! defines the wire shape we expect from `eth_subscribe` and
//! `alchemy_pendingTransactions`.

use serde::{Deserialize, Serialize};

/// minimal pending tx as seen on the mempool feed. fields are optional
/// because some providers omit them on early notifications.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PendingTx {
    pub hash: String,
    #[serde(default)]
    pub from: Option<String>,
    #[serde(default)]
    pub to: Option<String>,
    #[serde(default)]
    pub gas_price: Option<String>,
    #[serde(default)]
    pub max_fee_per_gas: Option<String>,
    #[serde(default)]
    pub max_priority_fee_per_gas: Option<String>,
    #[serde(default)]
    pub input: Option<String>,
    #[serde(default)]
    pub value: Option<String>,
    #[serde(default)]
    pub nonce: Option<String>,
}

impl PendingTx {
    /// parse from a json string. returns None on malformed input.
    pub fn from_json(s: &str) -> Option<Self> {
        serde_json::from_str(s).ok()
    }

    /// `true` when at least the hash and a sender are present.
    pub fn is_addressable(&self) -> bool {
        !self.hash.is_empty() && self.from.is_some()
    }
}

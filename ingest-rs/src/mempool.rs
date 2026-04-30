//! shred / streamed-tx subscriber types.
//!
//! the actual websocket / grpc loop lives in the binary target. this
//! module defines the wire shape we expect from yellowstone-grpc and
//! jito-shredstream-proxy notifications.

use serde::{Deserialize, Serialize};

/// minimal solana transaction as seen on the geyser / shredstream feed.
/// fields are optional because some providers omit them on early
/// notifications (pre-execution shreds).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct StreamedTx {
    pub signature: String,
    #[serde(default)]
    pub slot: Option<u64>,
    #[serde(default)]
    pub fee_payer: Option<String>,
    #[serde(default)]
    pub compute_unit_price: Option<u64>,
    #[serde(default)]
    pub compute_units: Option<u64>,
    #[serde(default)]
    pub message_b58: Option<String>,
    #[serde(default)]
    pub recent_blockhash: Option<String>,
}

impl StreamedTx {
    /// parse from a json string. returns None on malformed input.
    pub fn from_json(s: &str) -> Option<Self> {
        serde_json::from_str(s).ok()
    }

    /// `true` when at least the signature and a fee_payer are present.
    pub fn is_addressable(&self) -> bool {
        !self.signature.is_empty() && self.fee_payer.is_some()
    }
}

// alias kept for callers that imported PendingTx from v0.1.x. will be
// removed in a future minor release.
#[doc(hidden)]
pub type PendingTx = StreamedTx;

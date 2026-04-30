//! slot trace types.
//!
//! three trace modes are supported by the python binding. this crate
//! only models the data; the rpc plumbing lives in the binary target.

use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum TraceMode {
    GetBlock,
    Geyser,
    ShredStream,
}

impl TraceMode {
    pub fn as_str(&self) -> &'static str {
        match self {
            TraceMode::GetBlock => "getblock",
            TraceMode::Geyser => "geyser",
            TraceMode::ShredStream => "shredstream",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TracedTx {
    pub signature: String,
    pub fee_payer: String,
    pub slot: u64,
    #[serde(default)]
    pub jito_tip_lamports: u64,
    #[serde(default)]
    pub inner_ix_count: u32,
}

#[derive(Debug, Error)]
pub enum TraceError {
    #[error("rpc returned no result")]
    NoResult,
    #[error("malformed trace payload")]
    Malformed,
    #[error("trace mode `{0}` not supported by node")]
    UnsupportedMode(String),
}

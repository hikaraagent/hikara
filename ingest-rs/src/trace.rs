//! block trace types.
//!
//! three trace modes are supported by the python binding. this crate
//! only models the data; the rpc plumbing lives in the binary target.

use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum TraceMode {
    Debug,
    Parity,
    Rpc,
}

impl TraceMode {
    pub fn as_str(&self) -> &'static str {
        match self {
            TraceMode::Debug => "debug",
            TraceMode::Parity => "parity",
            TraceMode::Rpc => "rpc",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TracedTx {
    pub tx_hash: String,
    pub sender: String,
    pub to: String,
    #[serde(default)]
    pub coinbase_transfer_wei: u128,
    #[serde(default)]
    pub internal_calls: u32,
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

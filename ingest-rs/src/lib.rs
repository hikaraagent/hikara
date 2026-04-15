//! hakiri-ingest
//!
//! low-level ingest types and classifiers used by hakiri. kept minimal
//! and dependency-light. python core calls into this via pyo3 in v0.2.

#![forbid(unsafe_code)]
#![deny(rust_2018_idioms)]

pub mod bundle;
pub mod mempool;
pub mod trace;

pub use bundle::{classify_sandwich, Bundle, BundleClassification, SwapLeg};
pub use mempool::PendingTx;
pub use trace::{TraceMode, TracedTx};

/// crate version. matches Cargo.toml.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

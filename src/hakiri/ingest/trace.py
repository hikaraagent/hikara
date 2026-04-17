"""block tracer.

three modes:
  - debug: debug_traceblockbynumber (geth/erigon). full call tree, expensive.
  - parity: trace_block (parity-style nodes, openethereum). cheap, partial.
  - rpc: eth_getlogs only. no internal txs. covers ~80% of dex mev.

selects based on settings.trace_mode. stub here, real implementation
follows in v0.2.

TODO(0xnova): wire all three trace modes. tracking issue: #21.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal

TraceMode = Literal["debug", "parity", "rpc"]


@dataclass
class TracedTx:
    tx_hash: str
    sender: str
    to: str
    coinbase_transfer_wei: int = 0
    internal_calls: int = 0


async def trace_block(
    http_url: str, block_number: int, mode: TraceMode = "rpc"
) -> List[TracedTx]:
    """fetch block trace in the requested mode.

    stub returns an empty list. real implementation switches on `mode`
    and constructs the rpc payload.
    """
    _ = http_url, block_number, mode
    return []

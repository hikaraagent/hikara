"""block tracer.

solana exposes the same data via two rpc patterns:
  - getBlock (with full transactions): canonical, slow.
  - getTransaction (per signature): used to enrich a single tx.
  - geyser stream (via ingest-rs): low-latency, subscription-based.

selects based on settings. stub here, real implementation follows in v0.3.

TODO(0xnova): wire all three modes. tracking issue: #21.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal


TraceMode = Literal["getblock", "geyser", "shredstream"]


@dataclass
class TracedTx:
    signature: str
    sender: str
    slot: int
    jito_tip_lamports: int = 0
    inner_ix_count: int = 0


async def trace_slot(
    rpc_url: str, slot: int, mode: TraceMode = "getblock"
) -> List[TracedTx]:
    """fetch slot trace in the requested mode.

    stub returns an empty list. real implementation switches on `mode`
    and constructs the rpc payload.
    """
    _ = rpc_url, slot, mode
    return []

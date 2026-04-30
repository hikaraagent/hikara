"""jito block engine bundle reader.

pulls public bundle delivery data from the jito block engine api. used
to attribute slots to bundle-paying searchers and to find tip transfers
without needing call traces.

stub. polls the bundle stats endpoint with httpx. for the demo we
return an empty list.

TODO(0xnova): real polling, rate limiting, and de-dup across endpoints.
tracking issue: #18.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class JitoBundleTrace:
    bundle_id: str
    slot: int
    block_hash: str
    leader: str
    tip_lamports: int
    tx_count: int


async def fetch_recent_bundles(
    block_engine_url: str, limit: int = 100
) -> List[JitoBundleTrace]:
    """fetch recent landed bundles from the jito block engine.

    stub returns an empty list. real call uses httpx.AsyncClient.
    """
    _ = block_engine_url, limit
    return []

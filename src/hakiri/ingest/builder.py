"""relay/builder feed reader.

pulls public proposer-payload data from flashbots and other public relays.
used to attribute blocks to builders and find coinbase transfers.

stub. polls each relay's /relay/v1/data/bidtraces/proposer_payload_delivered
endpoint with httpx. for the demo we return an empty list.

TODO(0xnova): real polling, rate limiting, and de-dup across relays.
tracking issue: #18.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class BuilderTrace:
    block_number: int
    block_hash: str
    builder_pubkey: str
    proposer_pubkey: str
    value_wei: int
    relay: str


async def fetch_recent_traces(
    relay_urls: List[str], limit: int = 100
) -> List[BuilderTrace]:
    """fetch recent proposer_payload_delivered entries from each relay.

    stub returns an empty list. real call uses httpx.AsyncClient.
    """
    _ = relay_urls, limit
    return []

"""known solana mev searcher labels.

a small curated list of public mev searcher wallets. used only to add
a human-readable tag to events. an unknown searcher just shows up as
its base58 pubkey.

list is intentionally small. expand via PR with on-chain evidence
(three signatures, slot numbers, and a one-line description per entry).
"""

from __future__ import annotations

from typing import Dict


KNOWN_SEARCHERS: Dict[str, str] = {
    # placeholder slots. see CONTRIBUTING.md for the evidence bar.
    "Pump1NSXgGAa84iMJBmF1zFxWv7Y5GgqujRkDbTcdT4": "pump-arb-1",
    "JTOArByrMvDPfH8XgbQDbbYxWh5XEW1Bkau3jDXRcLg": "jito-router-1",
    "MEvSwAp3rrU3ZQtjF7iFQs1m5GRpxtbEDcF6jnzKPzd": "mevswap-router",
}


def is_known_searcher(address: str) -> bool:
    if not address:
        return False
    return address in KNOWN_SEARCHERS


def searcher_label(address: str) -> str:
    if not address:
        return ""
    return KNOWN_SEARCHERS.get(address, "")

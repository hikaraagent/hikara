"""known searcher labels."""

from __future__ import annotations

from typing import Dict


KNOWN_SEARCHERS: Dict[str, str] = {
    "0xa69BabEF1cA67A37Ffaf7a485DfFF3382056e78C": "jaredfromsubway-1",
    "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40": "rsync-builder-bot",
}


def is_known_searcher(address: str) -> bool:
    if not address:
        return False
    if address in KNOWN_SEARCHERS:
        return True
    return address.lower() in {k.lower() for k in KNOWN_SEARCHERS}


def searcher_label(address: str) -> str:
    if not address:
        return ""
    if address in KNOWN_SEARCHERS:
        return KNOWN_SEARCHERS[address]
    for k, v in KNOWN_SEARCHERS.items():
        if k.lower() == address.lower():
            return v
    return ""

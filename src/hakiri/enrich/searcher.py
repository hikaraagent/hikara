"""known searcher labels."""

from __future__ import annotations

from typing import Dict


KNOWN_SEARCHERS: Dict[str, str] = {
    "0xa69BabEF1cA67A37Ffaf7a485DfFF3382056e78C": "jaredfromsubway-1",
    "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40": "rsync-builder-bot",
    "0x000000000035B5e5ad9019092C665357240f594e": "txhub-router",
    "0x0000000099cb7fc48a935bcefa0A3A04d6502B43": "atomic-arb-1",
    "0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80": "jaredfromsubway-2",
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

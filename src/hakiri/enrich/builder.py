"""builder attribution."""

from __future__ import annotations

from typing import Dict, Optional


KNOWN_BUILDERS: Dict[str, str] = {
    "0x690B9A9E9aa1C9dB991C7721a92d351Db4FaC990": "builder0x69",
    "0xE8DDAd86796E7416c0E62D1Bf90e54a4C2Dabd28": "rsync-builder",
    "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5": "beaverbuild",
}


def attribute_builder(coinbase: str) -> Optional[str]:
    if not coinbase:
        return None
    if coinbase in KNOWN_BUILDERS:
        return KNOWN_BUILDERS[coinbase]
    for k, v in KNOWN_BUILDERS.items():
        if k.lower() == coinbase.lower():
            return v
    return None

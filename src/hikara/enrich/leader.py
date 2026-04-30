"""leader (validator) attribution.

each solana slot is produced by exactly one validator (the leader).
the leader is fetched from the leader schedule and stable for the slot.
this module provides a lookup of well-known validators by their
identity pubkey so events can be tagged with a friendly name.
"""

from __future__ import annotations

from typing import Dict, Optional

KNOWN_LEADERS: Dict[str, str] = {
    # high-stake public validators commonly seen as block leaders.
    "Certusm1sa411sMpV9FPqU5dXAYhmmhygvxJ23S6hJ24": "certus-one",
    "EAZpqLLuCkkSRKjVZTUZP41cV8kRk9ihVTpkjVj9wJYi": "everstake",
    "Dpvg4kCdMXJ5dvYCsK3QHN1XHkLkJk7Hf17VgQ7v9P3M": "shinobi-systems",
    "FigureFiNZHU7iyzv5fgWfgwGPsJzkrWeT3K4QmTGXDw": "figure-staking",
}


def attribute_leader(identity_pubkey: str) -> Optional[str]:
    """return human-readable validator name, or None if unknown."""
    if not identity_pubkey:
        return None
    return KNOWN_LEADERS.get(identity_pubkey)

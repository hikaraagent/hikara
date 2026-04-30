"""jito bundle and tip detection.

on solana, mev searchers pay validators for bundle inclusion via the
jito block engine. tips are sent to one of eight well-known tip
accounts. presence + size of a tip transfer is the strongest single
signal a transaction was part of a jito bundle.

reference: https://docs.jito.wtf
"""

from __future__ import annotations

from typing import Iterable


# the eight canonical jito tip accounts. tips can be sent to any of them.
JITO_TIP_ACCOUNTS = frozenset(
    {
        "96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5",
        "HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe",
        "Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY",
        "ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49",
        "DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDe9B",
        "ADuUkR4vqLUMWXxW9gh6D6L8pivKeVGvCEAoPmZ9JdfP",
        "DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL",
        "3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT",
    }
)


def find_jito_tip(transfers: Iterable[dict]) -> int:
    """sum lamports transferred to any jito tip account across the iter.

    each transfer is expected to expose `dst` (pubkey) and `lamports`
    (int). unknown shapes contribute 0.
    """
    total = 0
    for t in transfers:
        dst = t.get("dst")
        if dst not in JITO_TIP_ACCOUNTS:
            continue
        try:
            total += int(t.get("lamports") or 0)
        except (TypeError, ValueError):
            continue
    return total


def is_jito_tip_account(pubkey: str) -> bool:
    return pubkey in JITO_TIP_ACCOUNTS

"""coinbase transfer detection.

a coinbase transfer is a tx that sends eth directly to `block.coinbase`
inside its execution. searchers use this to pay the builder for inclusion
priority. presence + size of this transfer is the strongest single signal
that a tx is part of an mev bundle.

requires call-trace data (debug_traceTransaction or trace_block). without
traces, this returns 0 unless the tx itself is to the builder address.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Optional


def find_coinbase_transfer(
    internal_calls: Iterable[dict], block_coinbase: str
) -> int:
    """sum eth transferred to `block_coinbase` across internal calls.

    each internal_call is expected to expose `to` (address) and `value`
    (int wei). unknown shapes contribute 0.
    """
    if not block_coinbase:
        return 0
    target = block_coinbase.lower()
    total = 0
    for call in internal_calls:
        to = (call.get("to") or "").lower()
        if to != target:
            continue
        value = call.get("value") or 0
        try:
            total += int(value)
        except (TypeError, ValueError):
            continue
    return total


def coinbase_transfer_from_tx_value(
    to_address: Optional[str], block_coinbase: str, tx_value_wei: int
) -> int:
    """fallback when traces are not available. only catches direct sends."""
    if not to_address or not block_coinbase:
        return 0
    if to_address.lower() == block_coinbase.lower():
        return int(tx_value_wei or 0)
    return 0

"""orca whirlpool swap decoder.

whirlpools are concentrated-liquidity amms, similar in shape to
uniswap v3 but anchor-coded on solana. swaps are inner instructions
of the whirlpool program. we decode by recognizing the program id
and reading the paired token transfers.

returns a swap-shaped dict on success, None otherwise.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from hikara.decode.programs import ORCA_WHIRLPOOL


def decode_orca_swap(inner_ix: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """decode a single orca whirlpool inner instruction.

    returns a swap-shaped dict on success, None otherwise.
    """
    if inner_ix.get("program_id") != ORCA_WHIRLPOOL:
        return None

    accounts = inner_ix.get("accounts") or []
    if len(accounts) < 4:
        return None

    transfers = inner_ix.get("transfers") or []
    if len(transfers) < 2:
        return None

    in_t, out_t = transfers[0], transfers[1]

    return {
        "pool": accounts[0],
        "sender": accounts[1],
        "token_in": in_t.get("mint"),
        "token_out": out_t.get("mint"),
        "amount_in": int(in_t.get("amount") or 0),
        "amount_out": int(out_t.get("amount") or 0),
        "dex": "orca-whirlpool",
    }

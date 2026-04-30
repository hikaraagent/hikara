"""raydium amm v4 swap decoder.

raydium amm v4 is the canonical solana amm. swaps are encoded as
inner instructions inside a transaction. the program emits no log event
on success (logs are used only for errors), so decoding is done from
the inner instruction data + token transfer pairs.

this module reads the parsed inner-instruction shape:

    {
      "program_id": "<RAYDIUM_AMM_V4_PROGRAM_ID>",
      "data": "<base58 ix data>",
      "accounts": ["<pool>", "<user>", "<src_ata>", "<dst_ata>", ...],
      "transfers": [{"src": ..., "dst": ..., "amount": int, "mint": ...}, ...]
    }

returns a hakiri.core.types.SwapTx-shaped dict if it recognizes a swap,
None otherwise. the surrounding pipeline lifts dicts into SwapTx models.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from hakiri.decode.programs import RAYDIUM_AMM_V4

# first byte of raydium swap ixdata. swap variant disambiguates
# swapBaseIn (0x09) from swapBaseOut (0x0b).
SWAP_BASE_IN_TAG = 0x09
SWAP_BASE_OUT_TAG = 0x0B


def decode_raydium_swap(inner_ix: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """decode a single raydium amm v4 inner instruction.

    returns a swap-shaped dict on success, None otherwise.
    """
    if inner_ix.get("program_id") != RAYDIUM_AMM_V4:
        return None

    data = inner_ix.get("data") or b""
    if not data:
        return None
    tag = data[0] if isinstance(data, (bytes, bytearray)) else None
    if tag not in (SWAP_BASE_IN_TAG, SWAP_BASE_OUT_TAG):
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
        "dex": "raydium-amm-v4",
    }

"""uniswap v2 swap log decoder.

event signature:
  Swap(address sender, uint256 amount0In, uint256 amount1In,
       uint256 amount0Out, uint256 amount1Out, address to)
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from eth_abi import decode as abi_decode
from eth_utils import to_checksum_address

V2_SWAP_TOPIC = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"


def decode_v2_swap(log: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """decode a single uniswap v2 Swap log into a dict.

    returns None if topic doesn't match. shape is hashable into core.types.SwapTx
    after pool/token resolution.
    """
    topics = log.get("topics") or []
    if not topics or topics[0] != V2_SWAP_TOPIC:
        return None

    try:
        sender_topic = topics[1]
        to_topic = topics[2]
        sender = to_checksum_address("0x" + sender_topic[-40:])
        recipient = to_checksum_address("0x" + to_topic[-40:])
    except (IndexError, ValueError):
        return None

    data = log.get("data") or "0x"
    try:
        amount0_in, amount1_in, amount0_out, amount1_out = abi_decode(
            ["uint256", "uint256", "uint256", "uint256"], bytes.fromhex(data[2:])
        )
    except (ValueError, OverflowError):
        return None

    if amount0_in > 0 and amount1_out > 0:
        amount_in, amount_out, side = amount0_in, amount1_out, "0->1"
    elif amount1_in > 0 and amount0_out > 0:
        amount_in, amount_out, side = amount1_in, amount0_out, "1->0"
    else:
        return None

    return {
        "pool": log.get("address"),
        "sender": sender,
        "recipient": recipient,
        "amount_in": amount_in,
        "amount_out": amount_out,
        "side": side,
        "tx_hash": log.get("transactionHash"),
        "block_number": int(log.get("blockNumber", "0x0"), 16)
        if isinstance(log.get("blockNumber"), str)
        else log.get("blockNumber"),
        "log_index": int(log.get("logIndex", "0x0"), 16)
        if isinstance(log.get("logIndex"), str)
        else log.get("logIndex"),
    }

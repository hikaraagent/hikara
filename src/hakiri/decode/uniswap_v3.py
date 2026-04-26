"""uniswap v3 swap log decoder.

event signature:
  Swap(address sender, address recipient, int256 amount0, int256 amount1,
       uint160 sqrtPriceX96, uint128 liquidity, int24 tick)
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from eth_abi import decode as abi_decode
from eth_utils import to_checksum_address

V3_SWAP_TOPIC = "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"


def decode_v3_swap(log: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """decode a single uniswap v3 Swap log."""
    topics = log.get("topics") or []
    if not topics or topics[0] != V3_SWAP_TOPIC:
        return None

    try:
        sender = to_checksum_address("0x" + topics[1][-40:])
        recipient = to_checksum_address("0x" + topics[2][-40:])
    except (IndexError, ValueError):
        return None

    data = log.get("data") or "0x"
    try:
        amount0, amount1, sqrt_price_x96, liquidity, tick = abi_decode(
            ["int256", "int256", "uint160", "uint128", "int24"],
            bytes.fromhex(data[2:]),
        )
    except (ValueError, OverflowError):
        return None

    # malformed pools have been seen with both positive amounts; drop them.
    if amount0 > 0 and amount1 < 0:
        amount_in, amount_out, side = amount0, -amount1, "0->1"
    elif amount1 > 0 and amount0 < 0:
        amount_in, amount_out, side = amount1, -amount0, "1->0"
    else:
        return None

    return {
        "pool": log.get("address"),
        "sender": sender,
        "recipient": recipient,
        "amount_in": int(amount_in),
        "amount_out": int(amount_out),
        "side": side,
        "sqrt_price_x96": int(sqrt_price_x96),
        "liquidity": int(liquidity),
        "tick": int(tick),
        "tx_hash": log.get("transactionHash"),
        "block_number": int(log.get("blockNumber", "0x0"), 16)
        if isinstance(log.get("blockNumber"), str)
        else log.get("blockNumber"),
        "log_index": int(log.get("logIndex", "0x0"), 16)
        if isinstance(log.get("logIndex"), str)
        else log.get("logIndex"),
    }

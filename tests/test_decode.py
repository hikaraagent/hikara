"""tests for hakiri.decode (uniswap v2/v3 log decoders + routers)."""

from __future__ import annotations

from eth_abi import encode as abi_encode

from hakiri.decode.routers import is_known_router, router_label
from hakiri.decode.uniswap_v2 import V2_SWAP_TOPIC, decode_v2_swap
from hakiri.decode.uniswap_v3 import V3_SWAP_TOPIC, decode_v3_swap


def _addr_topic(addr: str) -> str:
    return "0x" + "0" * 24 + addr.lower().replace("0x", "")


def test_v2_swap_decode_zero_to_one() -> None:
    sender = "0x1111111111111111111111111111111111111111"
    to = "0x2222222222222222222222222222222222222222"
    data = "0x" + abi_encode(
        ["uint256", "uint256", "uint256", "uint256"], [10**18, 0, 0, 5_000_000]
    ).hex()
    log = {
        "topics": [V2_SWAP_TOPIC, _addr_topic(sender), _addr_topic(to)],
        "data": data,
        "address": "0xpool",
        "transactionHash": "0xtx",
        "blockNumber": "0x1",
        "logIndex": "0x0",
    }
    out = decode_v2_swap(log)
    assert out is not None
    assert out["amount_in"] == 10**18
    assert out["amount_out"] == 5_000_000
    assert out["side"] == "0->1"


def test_v2_swap_decode_returns_none_on_other_topic() -> None:
    log = {"topics": ["0xdeadbeef"], "data": "0x", "address": "0xpool"}
    assert decode_v2_swap(log) is None


def test_v3_swap_decode_one_to_zero() -> None:
    sender = "0x1111111111111111111111111111111111111111"
    to = "0x2222222222222222222222222222222222222222"
    data = "0x" + abi_encode(
        ["int256", "int256", "uint160", "uint128", "int24"],
        [-(10**18), 5_000_000, 79228162514264337593543950336, 100, 1],
    ).hex()
    log = {
        "topics": [V3_SWAP_TOPIC, _addr_topic(sender), _addr_topic(to)],
        "data": data,
        "address": "0xpool",
        "transactionHash": "0xtx",
        "blockNumber": "0x1",
        "logIndex": "0x0",
    }
    out = decode_v3_swap(log)
    assert out is not None
    assert out["side"] == "1->0"


def test_known_routers_have_labels() -> None:
    uni_v2 = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    assert is_known_router(uni_v2)
    assert router_label(uni_v2) == "uniswap-v2-router"


def test_unknown_router_returns_empty_label() -> None:
    assert not is_known_router("0xdead")
    assert router_label("0xdead") == ""

"""tests for hakiri.core.classify."""

from __future__ import annotations

from hakiri.core.classify import classify_block
from hakiri.core.types import EventKind, SwapTx, Verdict

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
POOL = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
SEARCHER = "0xa69BabEF1cA67A37Ffaf7a485DfFF3382056e78C"
VICTIM = "0xCAFE8888888888888888888888888888888888AA"


def _swap(idx: int, sender: str, t_in: str, t_out: str, **kwargs) -> SwapTx:
    return SwapTx(
        tx_hash=f"0x{idx:064x}",
        block_number=21_000_000,
        tx_index=idx,
        sender=sender,
        pool=POOL,
        token_in=t_in,
        token_out=t_out,
        amount_in=10**18,
        amount_out=10**6,
        gas_price_wei=20_000_000_000,
        gas_used=140_000,
        **kwargs,
    )


def test_sandwich_detected() -> None:
    swaps = [
        _swap(0, SEARCHER, WETH, USDC, coinbase_transfer_wei=10**16),
        _swap(1, VICTIM, WETH, USDC),
        _swap(2, SEARCHER, USDC, WETH, coinbase_transfer_wei=10**16),
    ]
    result = classify_block(swaps, block_number=21_000_000)

    assert len(result.events) == 1
    assert result.events[0].kind == EventKind.SANDWICH
    assert result.verdict in (Verdict.LIKELY, Verdict.CONFIRMED)
    assert "SAND-01" in result.rules_fired
    assert result.events[0].victims[0].tx_hash == swaps[1].tx_hash


def test_no_sandwich_when_searcher_differs() -> None:
    other = "0x111111111111111111111111111111111111aaaa"
    swaps = [
        _swap(0, SEARCHER, WETH, USDC),
        _swap(1, VICTIM, WETH, USDC),
        _swap(2, other, USDC, WETH),
    ]
    result = classify_block(swaps, block_number=21_000_000)
    assert all(e.kind != EventKind.SANDWICH for e in result.events)


def test_no_events_on_empty_block() -> None:
    result = classify_block([], block_number=21_000_000)
    assert result.events == []
    assert result.verdict == Verdict.NOISE


def test_backrun_detected() -> None:
    other = "0x222222222222222222222222222222222222bbbb"
    swaps = [
        _swap(0, VICTIM, WETH, USDC),
        _swap(1, other, WETH, USDC),
    ]
    result = classify_block(swaps, block_number=21_000_000)
    assert any(e.kind == EventKind.BACKRUN for e in result.events)


def test_swap_order_independence() -> None:
    swaps = [
        _swap(2, SEARCHER, USDC, WETH),
        _swap(0, SEARCHER, WETH, USDC),
        _swap(1, VICTIM, WETH, USDC),
    ]
    result = classify_block(swaps, block_number=21_000_000)
    assert len(result.events) == 1
    assert result.events[0].kind == EventKind.SANDWICH

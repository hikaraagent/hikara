"""tests for hikara.core.classify."""

from __future__ import annotations

from hikara.core.classify import classify_slot
from hikara.core.types import EventKind, SwapTx, Verdict

SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
POOL = "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"
SEARCHER = "JTOArByrMvDPfH8XgbQDbbYxWh5XEW1Bkau3jDXRcLg"
VICTIM = "VicT1mw411111111111111111111111111111111111"


def _swap(idx: int, sender: str, t_in: str, t_out: str, **kwargs) -> SwapTx:
    return SwapTx(
        signature=f"Sig{idx:061d}",
        slot=287_000_000,
        tx_index=idx,
        sender=sender,
        pool=POOL,
        token_in=t_in,
        token_out=t_out,
        amount_in=10**9,
        amount_out=10**6,
        compute_unit_price=20_000,
        compute_units=140_000,
        **kwargs,
    )


def test_sandwich_detected() -> None:
    swaps = [
        _swap(0, SEARCHER, SOL, USDC, jito_tip_lamports=10**6),
        _swap(1, VICTIM, SOL, USDC),
        _swap(2, SEARCHER, USDC, SOL, jito_tip_lamports=10**6),
    ]
    result = classify_slot(swaps, slot=287_000_000)

    assert len(result.events) == 1
    assert result.events[0].kind == EventKind.SANDWICH
    assert result.verdict in (Verdict.LIKELY, Verdict.CONFIRMED)
    assert "SAND-01" in result.rules_fired
    assert result.events[0].victims[0].signature == swaps[1].signature


def test_no_sandwich_when_searcher_differs() -> None:
    other = "Other11111111111111111111111111111111111111"
    swaps = [
        _swap(0, SEARCHER, SOL, USDC),
        _swap(1, VICTIM, SOL, USDC),
        _swap(2, other, USDC, SOL),
    ]
    result = classify_slot(swaps, slot=287_000_000)
    assert all(e.kind != EventKind.SANDWICH for e in result.events)


def test_no_events_on_empty_slot() -> None:
    result = classify_slot([], slot=287_000_000)
    assert result.events == []
    assert result.verdict == Verdict.NOISE


def test_backrun_detected() -> None:
    other = "Bckr1n1111111111111111111111111111111111111"
    swaps = [
        _swap(0, VICTIM, SOL, USDC),
        _swap(1, other, SOL, USDC),
    ]
    result = classify_slot(swaps, slot=287_000_000)
    assert any(e.kind == EventKind.BACKRUN for e in result.events)


def test_swap_order_independence() -> None:
    swaps = [
        _swap(2, SEARCHER, USDC, SOL),
        _swap(0, SEARCHER, SOL, USDC),
        _swap(1, VICTIM, SOL, USDC),
    ]
    result = classify_slot(swaps, slot=287_000_000)
    assert len(result.events) == 1
    assert result.events[0].kind == EventKind.SANDWICH

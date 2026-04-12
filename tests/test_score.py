"""tests for hakiri.core.score."""

from __future__ import annotations

from hakiri.core.score import CONFIDENCE_CEILING, score_event
from hakiri.core.types import Bundle, Event, EventKind, SwapTx, Verdict, Victim


def _bundle_event(kind: EventKind, **kwargs) -> Event:
    return Event(
        kind=kind,
        block_number=21_000_000,
        bundle=Bundle(block_number=21_000_000, searcher="0xabc", txs=[]),
        **kwargs,
    )


def test_score_capped_at_ceiling() -> None:
    swap = SwapTx(
        tx_hash="0xa",
        block_number=21_000_000,
        tx_index=0,
        sender="0xabc",
        pool="0xpool",
        token_in="0xt1",
        token_out="0xt2",
        amount_in=1,
        amount_out=1,
        gas_price_wei=1,
        gas_used=1,
    )
    ev = Event(
        kind=EventKind.SANDWICH,
        block_number=21_000_000,
        bundle=Bundle(
            block_number=21_000_000,
            searcher="0xabc",
            txs=[swap, swap],
            coinbase_transfer_wei=10**18,
        ),
        coinbase_transfer_wei=10**18,
        searcher="0xabc",
        builder="0xabc",
        victims=[Victim(tx_hash="0xv", sender="0xv")],
    )
    s = score_event(ev)
    assert s.confidence <= CONFIDENCE_CEILING
    assert s.verdict == Verdict.CONFIRMED


def test_unclassified_has_low_confidence() -> None:
    ev = _bundle_event(EventKind.UNCLASSIFIED)
    s = score_event(ev)
    assert s.confidence < 0.5
    assert s.verdict in (Verdict.NOISE, Verdict.SUSPECTED)


def test_reasons_are_traced() -> None:
    ev = _bundle_event(EventKind.SANDWICH, coinbase_transfer_wei=10**16)
    s = score_event(ev)
    assert any("base[sandwich]" in r for r in s.reasons)
    assert any("coinbase_transfer>0" in r for r in s.reasons)

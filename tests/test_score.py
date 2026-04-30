"""tests for hakiri.core.score."""

from __future__ import annotations

from hakiri.core.score import CONFIDENCE_CEILING, score_event
from hakiri.core.types import Bundle, Event, EventKind, SwapTx, Verdict, Victim


def _bundle_event(kind: EventKind, **kwargs) -> Event:
    return Event(
        kind=kind,
        slot=287_000_000,
        bundle=Bundle(slot=287_000_000, searcher="JTOarbi", txs=[]),
        **kwargs,
    )


def test_score_capped_at_ceiling() -> None:
    swap = SwapTx(
        signature="SigA",
        slot=287_000_000,
        tx_index=0,
        sender="JTOarbi",
        pool="poolA",
        token_in="t1",
        token_out="t2",
        amount_in=1,
        amount_out=1,
        compute_unit_price=1,
        compute_units=1,
    )
    ev = Event(
        kind=EventKind.SANDWICH,
        slot=287_000_000,
        bundle=Bundle(
            slot=287_000_000,
            searcher="JTOarbi",
            txs=[swap, swap],
            jito_tip_lamports=10**8,
        ),
        jito_tip_lamports=10**8,
        searcher="JTOarbi",
        leader="JTOarbi",
        victims=[Victim(signature="SigVictim", sender="VicSender")],
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
    ev = _bundle_event(EventKind.SANDWICH, jito_tip_lamports=10**6)
    s = score_event(ev)
    assert any("base[sandwich]" in r for r in s.reasons)
    assert any("jito_tip>0" in r for r in s.reasons)

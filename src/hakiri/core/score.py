"""rule-based scorer.

returns a confidence in [0.0, 0.95]. capped at 0.95 by design.
hakiri is a detector, not an oracle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from hakiri.core.types import Event, EventKind, Verdict

CONFIDENCE_CEILING = 0.95


@dataclass
class Score:
    """transparent score with the reasons that contributed to it."""

    confidence: float
    verdict: Verdict
    reasons: List[str]


# scoring base bands per kind. tweak with care.
def _base_for_kind(kind: EventKind) -> float:
    return {
        EventKind.SANDWICH: 0.70,
        EventKind.JIT: 0.65,
        EventKind.BACKRUN: 0.50,
        EventKind.LIQUIDATION: 0.55,
        EventKind.ARB: 0.45,
        EventKind.UNCLASSIFIED: 0.20,
    }.get(kind, 0.20)


def score_event(event: Event) -> Score:
    """rule-based confidence for a single event. no model calls."""
    reasons: List[str] = []
    score = _base_for_kind(event.kind)
    reasons.append(f"base[{event.kind.value}]={score:.2f}")

    if event.coinbase_transfer_wei > 0:
        score += 0.10
        reasons.append("coinbase_transfer>0:+0.10")

    if event.bundle and len(event.bundle.txs) >= 2:
        score += 0.05
        reasons.append("bundle.txs>=2:+0.05")

    if event.victims:
        score += 0.05
        reasons.append("victims_present:+0.05")

    if event.searcher and event.searcher == event.builder:
        score += 0.05
        reasons.append("searcher==builder:+0.05")

    score = min(score, CONFIDENCE_CEILING)

    if score >= 0.85:
        verdict = Verdict.CONFIRMED
    elif score >= 0.65:
        verdict = Verdict.LIKELY
    elif score >= 0.40:
        verdict = Verdict.SUSPECTED
    else:
        verdict = Verdict.NOISE

    return Score(confidence=round(score, 3), verdict=verdict, reasons=reasons)

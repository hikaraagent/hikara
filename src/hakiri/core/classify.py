"""slot-level mev classifier.

input: a list of decoded swaps from one slot, ordered by tx_index.
output: zero or more events. the same swap can appear in only one event.

heuristics are intentionally simple and additive. each rule has an id
that is referenced from docs/heuristics.md. when a rule fires, its id
is appended to event.notes for traceability.

this module is pure. no rpc, no clock, no io.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from hakiri.core.types import Bundle, Event, EventKind, SwapTx, Verdict, Victim


@dataclass
class Classification:
    """wrapped result so callers can see what fired without re-running rules."""

    events: List[Event]
    rules_fired: List[str]
    verdict: Verdict


def _group_by_pool(swaps: List[SwapTx]) -> dict:
    by_pool: dict = defaultdict(list)
    for s in swaps:
        by_pool[s.pool].append(s)
    return by_pool


def _is_sandwich_pattern(a: SwapTx, b: SwapTx, c: SwapTx) -> bool:
    """front-run, victim, back-run on same pool. opposite directions for a/c."""
    same_pool = a.pool == b.pool == c.pool
    same_searcher = a.sender == c.sender and a.sender != b.sender
    opposite_dirs = (
        a.token_in == b.token_in
        and a.token_out == b.token_out
        and c.token_in == b.token_out
        and c.token_out == b.token_in
    )
    ordered = a.tx_index < b.tx_index < c.tx_index
    return same_pool and same_searcher and opposite_dirs and ordered


def _detect_sandwiches(swaps: List[SwapTx], slot: int) -> List[Event]:
    """rule SAND-01: a -> victim -> c on same pool, same searcher, opposite directions."""
    events: List[Event] = []
    n = len(swaps)
    if n < 3:
        return events

    used: set = set()
    for i in range(n - 2):
        if i in used:
            continue
        for k in range(i + 2, n):
            if k in used:
                continue
            for j in range(i + 1, k):
                if j in used:
                    continue
                if _is_sandwich_pattern(swaps[i], swaps[j], swaps[k]):
                    bundle = Bundle(
                        slot=slot,
                        searcher=swaps[i].sender,
                        txs=[swaps[i], swaps[k]],
                        jito_tip_lamports=(
                            swaps[i].jito_tip_lamports
                            + swaps[k].jito_tip_lamports
                        ),
                        compute_units=swaps[i].compute_units + swaps[k].compute_units,
                    )
                    victim = Victim(
                        signature=swaps[j].signature, sender=swaps[j].sender
                    )
                    events.append(
                        Event(
                            kind=EventKind.SANDWICH,
                            slot=slot,
                            bundle=bundle,
                            victims=[victim],
                            searcher=swaps[i].sender,
                            jito_tip_lamports=bundle.jito_tip_lamports,
                            notes=["SAND-01"],
                        )
                    )
                    used.update({i, j, k})
                    break
            else:
                continue
            break
    return events


def _detect_backruns(swaps: List[SwapTx], slot: int) -> List[Event]:
    """rule BACK-01: tx (n) by user shifts price, tx (n+1) by different sender same pool same direction = backrun arb candidate."""
    events: List[Event] = []
    for i in range(len(swaps) - 1):
        a, b = swaps[i], swaps[i + 1]
        if a.pool != b.pool:
            continue
        if a.sender == b.sender:
            continue
        if a.token_in != b.token_in or a.token_out != b.token_out:
            continue
        events.append(
            Event(
                kind=EventKind.BACKRUN,
                slot=slot,
                bundle=Bundle(
                    slot=slot,
                    searcher=b.sender,
                    txs=[b],
                    jito_tip_lamports=b.jito_tip_lamports,
                    compute_units=b.compute_units,
                ),
                searcher=b.sender,
                jito_tip_lamports=b.jito_tip_lamports,
                notes=["BACK-01"],
            )
        )
    return events


def classify_slot(swaps: List[SwapTx], slot: int) -> Classification:
    """run all heuristics over a slot's swaps. returns events + which rules fired."""
    rules: List[str] = []

    swaps = sorted(swaps, key=lambda s: s.tx_index)

    sandwiches = _detect_sandwiches(swaps, slot)
    if sandwiches:
        rules.append("SAND-01")

    used_swaps = set()
    for ev in sandwiches:
        if ev.bundle:
            for tx in ev.bundle.txs:
                used_swaps.add(tx.signature)
        for v in ev.victims:
            used_swaps.add(v.signature)

    remaining = [s for s in swaps if s.signature not in used_swaps]
    backruns = _detect_backruns(remaining, slot)
    if backruns:
        rules.append("BACK-01")

    events = sandwiches + backruns

    if not events:
        verdict = Verdict.NOISE
    elif len(rules) >= 2:
        verdict = Verdict.CONFIRMED
    else:
        verdict = Verdict.LIKELY

    return Classification(events=events, rules_fired=rules, verdict=verdict)


# legacy alias for backward compatibility within the python codebase only.
# external callers should use classify_slot directly.
classify_block = classify_slot

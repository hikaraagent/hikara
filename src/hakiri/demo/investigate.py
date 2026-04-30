"""demo investigate: walks the full pipeline on one synthetic slot.

prints decoded swaps, classification rules fired, scoring breakdown,
and final verdict per event. used in screencasts to show the ladder
from raw inner instructions to verdict.
"""

from __future__ import annotations

from rich.console import Console

from hakiri.core.classify import classify_slot
from hakiri.core.score import score_event
from hakiri.demo.scan import fixture_swaps


def run_demo_investigate() -> None:
    c = Console()

    swaps = fixture_swaps()
    c.rule("step 1. decoded swaps")
    for s in swaps:
        c.print(
            f"  slot {s.slot} idx {s.tx_index}  "
            f"sender {s.sender[:10]}...  "
            f"pool {s.pool[:10]}...  "
            f"in {s.amount_in:_}  out {s.amount_out:_}"
        )

    c.rule("step 2. classifier rules")
    result = classify_slot(swaps, slot=287000000)
    c.print(f"  rules fired: {result.rules_fired or '[none]'}")
    c.print(f"  slot verdict: {result.verdict.value}")
    c.print(f"  events found: {len(result.events)}")

    c.rule("step 3. score per event")
    for ev in result.events:
        s = score_event(ev)
        c.print(f"  {ev.kind.value} slot {ev.slot}")
        for r in s.reasons:
            c.print(f"    {r}", markup=False)
        c.print(f"    -> verdict={s.verdict.value} conf={s.confidence:.3f}")

    c.rule("done")

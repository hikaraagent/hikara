"""minimal scan example: feed swaps in, get scored events out.

run with:
    python examples/basic_scan.py
"""

from __future__ import annotations

from hikara.core.classify import classify_slot
from hikara.core.score import score_event
from hikara.demo.scan import fixture_swaps
from hikara.output.stdout import StdoutSink


def main() -> None:
    sink = StdoutSink()
    swaps = fixture_swaps()
    result = classify_slot(swaps, slot=287_000_000)
    for ev in result.events:
        sink.emit(ev, score_event(ev))


if __name__ == "__main__":
    main()

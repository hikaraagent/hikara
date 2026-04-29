"""minimal scan example: feed swaps in, get scored events out.

run with:
    python examples/basic_scan.py
"""

from __future__ import annotations

from hakiri.core.classify import classify_block
from hakiri.core.score import score_event
# fixture is the canonical sandwich block used in tests.
from hakiri.demo.scan import fixture_swaps
from hakiri.output.stdout import StdoutSink


def main() -> None:
    sink = StdoutSink()
    swaps = fixture_swaps()
    result = classify_block(swaps, block_number=21_000_000)
    for ev in result.events:
        sink.emit(ev, score_event(ev))


if __name__ == "__main__":
    main()

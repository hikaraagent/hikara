"""smoke tests for the demo subcommand."""

from __future__ import annotations

from hikara.demo.investigate import run_demo_investigate
from hikara.demo.scan import fixture_swaps, run_demo_scan


def test_fixture_has_sandwich_pattern() -> None:
    swaps = fixture_swaps()
    assert len(swaps) >= 3


def test_demo_scan_emits_at_least_one_event() -> None:
    events = run_demo_scan()
    assert events, "demo scan should produce at least one classified event"


def test_demo_investigate_runs() -> None:
    run_demo_investigate()

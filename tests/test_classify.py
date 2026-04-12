"""tests for hakiri.core.classify."""

from __future__ import annotations

from hakiri.core.classify import classify_block
from hakiri.core.types import Verdict


def test_no_events_on_empty_block() -> None:
    result = classify_block([], block_number=21_000_000)
    assert result.events == []
    assert result.verdict == Verdict.NOISE

"""tests for hakiri.output sinks (jsonl + stdout smoke)."""

from __future__ import annotations

import json

from hakiri.core.score import score_event
from hakiri.core.types import Bundle, Event, EventKind, SwapTx, Victim
from hakiri.output.jsonl import JsonlSink
from hakiri.output.stdout import StdoutSink


def _event() -> Event:
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
    return Event(
        kind=EventKind.SANDWICH,
        block_number=21_000_000,
        bundle=Bundle(block_number=21_000_000, searcher="0xabc", txs=[swap]),
        victims=[Victim(tx_hash="0xv", sender="0xv")],
    )


def test_jsonl_sink_writes_one_line(tmp_path) -> None:
    path = tmp_path / "events.jsonl"
    sink = JsonlSink(path)
    ev = _event()
    score = score_event(ev)
    sink.emit(ev, score)

    lines = path.read_text().strip().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert "event" in record
    assert "score" in record
    assert record["event"]["kind"] == "sandwich"


def test_stdout_sink_does_not_raise() -> None:
    sink = StdoutSink()
    ev = _event()
    score = score_event(ev)
    sink.emit(ev, score)

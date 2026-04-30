"""tests for hikara.output sinks (jsonl + stdout smoke)."""

from __future__ import annotations

import json

from hikara.core.score import score_event
from hikara.core.types import Bundle, Event, EventKind, SwapTx, Victim
from hikara.output.jsonl import JsonlSink
from hikara.output.stdout import StdoutSink


def _event() -> Event:
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
    return Event(
        kind=EventKind.SANDWICH,
        slot=287_000_000,
        bundle=Bundle(slot=287_000_000, searcher="JTOarbi", txs=[swap]),
        victims=[Victim(signature="SigVictim", sender="VicSender")],
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
    assert record["event"]["slot"] == 287_000_000


def test_stdout_sink_does_not_raise() -> None:
    sink = StdoutSink()
    ev = _event()
    score = score_event(ev)
    sink.emit(ev, score)

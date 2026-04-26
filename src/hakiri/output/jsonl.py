"""append-only jsonl sink.

one event per line. line is `{"event": ..., "score": ...}`. files are
opened in append mode and never truncated by hakiri.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from hakiri.core.score import Score
from hakiri.core.types import Event


class JsonlSink:
    def __init__(self, path: Union[str, Path]) -> None:
        self.path = Path(path)
        # callers may pass a path under a non-existent dir.
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: Event, score: Score) -> None:
        record = {
            "event": event.model_dump(mode="json"),
            "score": {
                "confidence": score.confidence,
                "verdict": score.verdict.value,
                "reasons": score.reasons,
            },
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
            fh.write("\n")

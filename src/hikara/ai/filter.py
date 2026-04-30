"""ai filter layer.

takes a low-confidence rule-based score and asks the model to either
upgrade, downgrade, or hold. never used as the primary scorer. cap stays
at 0.95 regardless of model output.

if ANTHROPIC_API_KEY is unset, AiFilter.is_available is False and callers
fall through to the rule-based score.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import structlog

from hikara.core.score import CONFIDENCE_CEILING, Score
from hikara.core.types import Event, Verdict

log = structlog.get_logger("hikara.ai.filter")


@dataclass
class FilterResult:
    confidence: float
    verdict: Verdict
    note: str


class AiFilter:
    def __init__(self, api_key: Optional[str], model: str) -> None:
        self.api_key = api_key
        self.model = model

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    async def review(self, event: Event, base: Score) -> FilterResult:
        """review a rule-based score. stub returns the base unchanged.

        TODO(senri): actual prompt + claude call. tracking issue: #27.
        """
        if not self.is_available:
            return FilterResult(
                confidence=base.confidence,
                verdict=base.verdict,
                note="ai_filter:disabled",
            )

        log.info(
            "ai.review.stub",
            model=self.model,
            kind=event.kind.value,
            base_conf=base.confidence,
        )
        capped = min(base.confidence, CONFIDENCE_CEILING)
        return FilterResult(
            confidence=capped,
            verdict=base.verdict,
            note="ai_filter:noop",
        )

"""webhook sink. POSTs each event to a configured URL.

failures are logged and swallowed. hikara is read-only; missed webhook
delivery never blocks classification.
"""

from __future__ import annotations

import httpx
import structlog

from hikara.core.score import Score
from hikara.core.types import Event

log = structlog.get_logger("hikara.output.webhook")


class WebhookSink:
    def __init__(self, url: str, timeout_s: float = 5.0) -> None:
        self.url = url
        self.timeout_s = timeout_s

    async def emit(self, event: Event, score: Score) -> None:
        payload = {
            "event": event.model_dump(mode="json"),
            "score": {
                "confidence": score.confidence,
                "verdict": score.verdict.value,
                "reasons": score.reasons,
            },
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                resp = await client.post(self.url, json=payload)
                if resp.status_code >= 400:
                    log.warning(
                        "webhook.bad_status",
                        url=self.url,
                        status=resp.status_code,
                    )
        except Exception as exc:
            log.warning("webhook.failed", url=self.url, error=str(exc))

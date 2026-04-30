"""feed events into a webhook sink.

run with:
    HIKARA_WEBHOOK_URL=https://your.webhook  python examples/webhook_sink.py
"""

from __future__ import annotations

import asyncio
import os

from hikara.core.classify import classify_block
from hikara.core.score import score_event
from hikara.demo.scan import fixture_swaps
from hikara.output.webhook import WebhookSink


async def main() -> None:
    url = os.environ.get("HIKARA_WEBHOOK_URL")
    if not url:
        print("HIKARA_WEBHOOK_URL not set. exiting.")
        return

    sink = WebhookSink(url)
    swaps = fixture_swaps()
    result = classify_block(swaps, block_number=21_000_000)
    for ev in result.events:
        await sink.emit(ev, score_event(ev))


if __name__ == "__main__":
    asyncio.run(main())

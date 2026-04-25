"""feed events into a webhook sink.

run with:
    HAKIRI_WEBHOOK_URL=https://your.webhook  python examples/webhook_sink.py
"""

from __future__ import annotations

import asyncio
import os

from hakiri.core.classify import classify_block
from hakiri.core.score import score_event
from hakiri.demo.scan import fixture_swaps
from hakiri.output.webhook import WebhookSink


async def main() -> None:
    url = os.environ.get("HAKIRI_WEBHOOK_URL")
    if not url:
        print("HAKIRI_WEBHOOK_URL not set. exiting.")
        return

    sink = WebhookSink(url)
    swaps = fixture_swaps()
    result = classify_block(swaps, block_number=21_000_000)
    for ev in result.events:
        await sink.emit(ev, score_event(ev))


if __name__ == "__main__":
    asyncio.run(main())

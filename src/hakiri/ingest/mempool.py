"""pending-tx subscriber.

stub. real ingest path runs in `ingest-rs/` (see crate docs). this module
exists so callers can run hakiri with python-only deps for demos and tests.

TODO(0xnova): replace with the rust binary once installable wheels exist
on pypi. tracking issue: #14.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Optional

import structlog

log = structlog.get_logger("hakiri.ingest.mempool")


async def subscribe_pending(
    ws_url: str, max_pending: Optional[int] = None
) -> AsyncIterator[dict]:
    """yield pending tx hashes as they arrive on the websocket.

    this is a stub. it logs intent and exits. replace with a real
    `eth_subscribe(["newPendingTransactions"])` once the rust ingest
    is wired in.
    """
    log.info("mempool.subscribe_pending.stub", ws_url=ws_url, max_pending=max_pending)
    if False:
        yield {}
    await asyncio.sleep(0)

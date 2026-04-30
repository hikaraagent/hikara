"""geyser / shredstream subscriber.

stub. real ingest path runs in `ingest-rs/` (see crate docs). this module
exists so callers can run hakiri with python-only deps for demos and tests.

geyser is solana's plugin interface for streaming account/slot/transaction
notifications. shredstream (jito-shredstream-proxy) gives sub-leader-level
latency by subscribing to TPU shreds before they're committed.

TODO(0xnova): wire `solana_geyser_plugin_interface` style subscriber via
the rust binary. tracking issue: #14.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Optional

import structlog

log = structlog.get_logger("hakiri.ingest.geyser")


async def subscribe_transactions(
    grpc_url: str, max_pending: Optional[int] = None
) -> AsyncIterator[dict]:
    """yield streamed transactions as they arrive on the geyser feed.

    this is a stub. it logs intent and exits. replace with a real
    yellowstone-grpc / shredstream subscription once the rust ingest
    is wired in.
    """
    log.info(
        "geyser.subscribe_transactions.stub",
        grpc_url=grpc_url,
        max_pending=max_pending,
    )
    if False:
        yield {}
    await asyncio.sleep(0)

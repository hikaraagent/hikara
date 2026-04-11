"""block-level mev classifier.

input: a list of decoded swaps from one block.
output: zero or more events.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from hakiri.core.types import Event, EventKind, SwapTx, Verdict


@dataclass
class Classification:
    events: List[Event]
    rules_fired: List[str]
    verdict: Verdict


def _group_by_pool(swaps):
    by_pool = defaultdict(list)
    for s in swaps:
        by_pool[s.pool].append(s)
    return by_pool


def classify_block(swaps, block_number: int) -> Classification:
    return Classification(events=[], rules_fired=[], verdict=Verdict.NOISE)

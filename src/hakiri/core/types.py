"""shared dataclasses and enums for the entire pipeline."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EventKind(str, Enum):
    SANDWICH = "sandwich"
    JIT = "jit"
    BACKRUN = "backrun"
    LIQUIDATION = "liquidation"
    ARB = "arb"
    UNCLASSIFIED = "unclassified"


class Verdict(str, Enum):
    CONFIRMED = "confirmed"
    LIKELY = "likely"
    SUSPECTED = "suspected"
    NOISE = "noise"


class SwapTx(BaseModel):
    tx_hash: str
    block_number: int
    tx_index: int
    sender: str
    pool: str
    token_in: str
    token_out: str
    amount_in: int
    amount_out: int
    gas_price_wei: int
    gas_used: int
    coinbase_transfer_wei: int = 0


class Victim(BaseModel):
    tx_hash: str
    sender: str
    realized_loss_wei: int = 0
    expected_amount_out: Optional[int] = None
    actual_amount_out: Optional[int] = None

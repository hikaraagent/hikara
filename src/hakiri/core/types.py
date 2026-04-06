"""shared dataclasses and enums for the entire pipeline.

kept dependency-free. only stdlib + pydantic. importing this from any
subpackage must not pull rpc, decoding, or scoring code.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class EventKind(str, Enum):
    SANDWICH = "sandwich"
    JIT = "jit"
    BACKRUN = "backrun"
    LIQUIDATION = "liquidation"
    ARB = "arb"
    UNCLASSIFIED = "unclassified"


class Verdict(str, Enum):
    """classifier confidence band shown to humans."""

    CONFIRMED = "confirmed"
    LIKELY = "likely"
    SUSPECTED = "suspected"
    NOISE = "noise"


class SwapTx(BaseModel):
    """one swap leg. dex-agnostic, decoded from logs."""

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
    """the user who got priced out, sandwiched, or jit'd."""

    tx_hash: str
    sender: str
    realized_loss_wei: int = 0
    expected_amount_out: Optional[int] = None
    actual_amount_out: Optional[int] = None

    @property
    def loss_eth(self) -> float:
        return self.realized_loss_wei / 1e18


class Bundle(BaseModel):
    """ordered group of txs from one searcher in one block."""

    block_number: int
    builder: Optional[str] = None
    searcher: Optional[str] = None
    txs: List[SwapTx] = Field(default_factory=list)
    coinbase_transfer_wei: int = 0
    gas_used: int = 0


class Event(BaseModel):
    """one mev event detected on a block. the unit hakiri reports on."""

    kind: EventKind
    block_number: int
    block_hash: Optional[str] = None
    bundle: Optional[Bundle] = None
    victims: List[Victim] = Field(default_factory=list)
    profit_wei: int = 0
    coinbase_transfer_wei: int = 0
    builder: Optional[str] = None
    searcher: Optional[str] = None
    notes: List[str] = Field(default_factory=list)

    @property
    def profit_eth(self) -> float:
        return self.profit_wei / 1e18

    @property
    def total_victim_loss_eth(self) -> float:
        return sum(v.loss_eth for v in self.victims)

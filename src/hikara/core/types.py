"""shared dataclasses and enums for the entire pipeline.

kept dependency-free. only stdlib + pydantic. importing this from any
subpackage must not pull rpc, decoding, or scoring code.

solana note. addresses are base58 pubkeys (32 bytes). amounts are token
raw units. native sol is in lamports (1 sol = 1e9 lamports).
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
    """one swap leg. dex-agnostic, decoded from inner instructions or logs."""

    signature: str
    slot: int
    tx_index: int
    sender: str
    pool: str
    token_in: str
    token_out: str
    amount_in: int
    amount_out: int
    compute_unit_price: int = 0
    compute_units: int = 0
    jito_tip_lamports: int = 0


class Victim(BaseModel):
    """the user who got priced out, sandwiched, or jit'd."""

    signature: str
    sender: str
    realized_loss_lamports: int = 0
    expected_amount_out: Optional[int] = None
    actual_amount_out: Optional[int] = None

    @property
    def loss_sol(self) -> float:
        return self.realized_loss_lamports / 1e9


class Bundle(BaseModel):
    """ordered group of txs from one searcher inside the same slot."""

    slot: int
    leader: Optional[str] = None
    searcher: Optional[str] = None
    txs: List[SwapTx] = Field(default_factory=list)
    jito_tip_lamports: int = 0
    compute_units: int = 0


class Event(BaseModel):
    """one mev event detected on a slot. the unit hikara reports on."""

    kind: EventKind
    slot: int
    block_hash: Optional[str] = None
    bundle: Optional[Bundle] = None
    victims: List[Victim] = Field(default_factory=list)
    profit_lamports: int = 0
    jito_tip_lamports: int = 0
    leader: Optional[str] = None
    searcher: Optional[str] = None
    notes: List[str] = Field(default_factory=list)

    @property
    def profit_sol(self) -> float:
        return self.profit_lamports / 1e9

    @property
    def total_victim_loss_sol(self) -> float:
        return sum(v.loss_sol for v in self.victims)

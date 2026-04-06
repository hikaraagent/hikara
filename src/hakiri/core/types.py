"""shared dataclasses and enums for the entire pipeline."""

from __future__ import annotations

from enum import Enum


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

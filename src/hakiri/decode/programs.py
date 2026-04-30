"""known solana dex / aggregator program ids.

base58-encoded pubkeys. used by the decoders to recognize their
target program and by the enricher to label aggregator-routed trades.

pull requests welcome. include three on-chain signatures as evidence.
"""

from __future__ import annotations

from typing import Dict


# core dexes
RAYDIUM_AMM_V4 = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
RAYDIUM_CLMM = "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK"
ORCA_WHIRLPOOL = "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc"
METEORA_DLMM = "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo"
METEORA_AMM = "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB"
LIFINITY_V2 = "2wT8Yq49kHgDzXuPxZSaeLaH1qbmGXtEyPy64bL7aD3c"

# aggregators / routers
JUPITER_V6 = "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"
JUPITER_V4 = "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB"

# launchpads (often source of victim swaps)
PUMP_FUN = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
RAYDIUM_LAUNCHPAD = "LanMV9sAd7wArD4vJFi2qDdfnVhFxYSUg6eADduJ3uj"

# jito programs
JITO_TIP_DISTRIBUTION = "4R3gSG8BpU4t19KYj8CfnbtRpnT8gtk4dvTHxVRwc2r7"
JITO_TIP_PAYMENT = "T1pyyaTNZsKv2WcRAB8oVnk93mLJw2XzjtVYqCsaHqt"


KNOWN_PROGRAMS: Dict[str, str] = {
    RAYDIUM_AMM_V4: "raydium-amm-v4",
    RAYDIUM_CLMM: "raydium-clmm",
    ORCA_WHIRLPOOL: "orca-whirlpool",
    METEORA_DLMM: "meteora-dlmm",
    METEORA_AMM: "meteora-amm",
    LIFINITY_V2: "lifinity-v2",
    JUPITER_V6: "jupiter-v6",
    JUPITER_V4: "jupiter-v4",
    PUMP_FUN: "pump-fun",
    RAYDIUM_LAUNCHPAD: "raydium-launchpad",
    JITO_TIP_DISTRIBUTION: "jito-tip-distribution",
    JITO_TIP_PAYMENT: "jito-tip-payment",
}


def is_known_program(program_id: str) -> bool:
    return program_id in KNOWN_PROGRAMS


def program_label(program_id: str) -> str:
    return KNOWN_PROGRAMS.get(program_id, "")

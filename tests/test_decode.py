"""tests for hakiri.decode (raydium + orca + program lookups)."""

from __future__ import annotations

from hakiri.decode.orca import decode_orca_swap
from hakiri.decode.programs import (
    ORCA_WHIRLPOOL,
    RAYDIUM_AMM_V4,
    is_known_program,
    program_label,
)
from hakiri.decode.raydium import (
    SWAP_BASE_IN_TAG,
    SWAP_BASE_OUT_TAG,
    decode_raydium_swap,
)

SOL_MINT = "So11111111111111111111111111111111111111112"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


def _ix(program_id: str, *, data: bytes, transfers: list, accounts: list) -> dict:
    return {
        "program_id": program_id,
        "data": data,
        "transfers": transfers,
        "accounts": accounts,
    }


def test_raydium_swap_decode_base_in() -> None:
    transfers = [
        {"src": "user_ata_sol", "dst": "pool_vault_sol", "amount": 10**9, "mint": SOL_MINT},
        {"src": "pool_vault_usdc", "dst": "user_ata_usdc", "amount": 30 * 10**6, "mint": USDC_MINT},
    ]
    accounts = ["pool_pda", "user_pubkey", "user_ata_sol", "user_ata_usdc"]
    out = decode_raydium_swap(
        _ix(RAYDIUM_AMM_V4, data=bytes([SWAP_BASE_IN_TAG]), transfers=transfers, accounts=accounts)
    )
    assert out is not None
    assert out["dex"] == "raydium-amm-v4"
    assert out["amount_in"] == 10**9
    assert out["amount_out"] == 30 * 10**6
    assert out["token_in"] == SOL_MINT
    assert out["token_out"] == USDC_MINT


def test_raydium_swap_returns_none_on_other_program() -> None:
    out = decode_raydium_swap(
        _ix("OtherProgram1111111", data=bytes([SWAP_BASE_OUT_TAG]), transfers=[], accounts=[])
    )
    assert out is None


def test_raydium_swap_returns_none_on_unknown_tag() -> None:
    out = decode_raydium_swap(
        _ix(RAYDIUM_AMM_V4, data=bytes([0x42]), transfers=[], accounts=[])
    )
    assert out is None


def test_orca_swap_decode() -> None:
    transfers = [
        {"src": "user_ata_sol", "dst": "pool_vault_sol", "amount": 5 * 10**8, "mint": SOL_MINT},
        {"src": "pool_vault_usdc", "dst": "user_ata_usdc", "amount": 15 * 10**6, "mint": USDC_MINT},
    ]
    accounts = ["whirlpool_pda", "user_pubkey", "user_ata_sol", "user_ata_usdc"]
    out = decode_orca_swap(
        _ix(ORCA_WHIRLPOOL, data=b"", transfers=transfers, accounts=accounts)
    )
    assert out is not None
    assert out["dex"] == "orca-whirlpool"
    assert out["amount_in"] == 5 * 10**8
    assert out["amount_out"] == 15 * 10**6


def test_orca_swap_returns_none_on_other_program() -> None:
    out = decode_orca_swap(_ix("OtherProgram", data=b"", transfers=[], accounts=[]))
    assert out is None


def test_known_programs_have_labels() -> None:
    assert is_known_program(RAYDIUM_AMM_V4)
    assert program_label(RAYDIUM_AMM_V4) == "raydium-amm-v4"
    assert program_label(ORCA_WHIRLPOOL) == "orca-whirlpool"


def test_unknown_program_returns_empty_label() -> None:
    assert not is_known_program("Unknown111111")
    assert program_label("Unknown111111") == ""

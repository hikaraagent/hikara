"""demo scan: produces a small batch of synthetic mev events.

used for screencasts and offline tests. the fixtures are intentionally
hand-rolled (not real chain data) so nothing here defames real wallets.
"""

from __future__ import annotations

from typing import List

from hakiri.core.classify import classify_block
from hakiri.core.score import score_event
from hakiri.core.types import Event, SwapTx
from hakiri.output.stdout import StdoutSink

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
POOL_USDC_WETH_V3 = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
SEARCHER_A = "0xa69BabEF1cA67A37Ffaf7a485DfFF3382056e78C"
SEARCHER_B = "0x000000000035B5e5ad9019092C665357240f594e"
VICTIM = "0xCAFE8888888888888888888888888888888888AA"


def fixture_swaps() -> List[SwapTx]:
    """canonical sandwich pattern + a backrun + a noise tx."""
    return [
        SwapTx(
            tx_hash="0xaa01",
            block_number=21000000,
            tx_index=0,
            sender=SEARCHER_A,
            pool=POOL_USDC_WETH_V3,
            token_in=WETH,
            token_out=USDC,
            amount_in=8 * 10**18,
            amount_out=24_000 * 10**6,
            gas_price_wei=30_000_000_000,
            gas_used=140_000,
            coinbase_transfer_wei=12 * 10**16,
        ),
        SwapTx(
            tx_hash="0xbb02",
            block_number=21000000,
            tx_index=1,
            sender=VICTIM,
            pool=POOL_USDC_WETH_V3,
            token_in=WETH,
            token_out=USDC,
            amount_in=2 * 10**18,
            amount_out=5_950 * 10**6,
            gas_price_wei=18_000_000_000,
            gas_used=160_000,
        ),
        SwapTx(
            tx_hash="0xcc03",
            block_number=21000000,
            tx_index=2,
            sender=SEARCHER_A,
            pool=POOL_USDC_WETH_V3,
            token_in=USDC,
            token_out=WETH,
            amount_in=24_500 * 10**6,
            amount_out=8_300 * 10**15,
            gas_price_wei=29_000_000_000,
            gas_used=145_000,
            coinbase_transfer_wei=8 * 10**16,
        ),
        SwapTx(
            tx_hash="0xdd04",
            block_number=21000000,
            tx_index=3,
            sender="0x1111111111111111111111111111111111111111",
            pool=POOL_USDC_WETH_V3,
            token_in=WETH,
            token_out=USDC,
            amount_in=1 * 10**17,
            amount_out=305 * 10**6,
            gas_price_wei=20_000_000_000,
            gas_used=120_000,
        ),
        SwapTx(
            tx_hash="0xee05",
            block_number=21000000,
            tx_index=4,
            sender=SEARCHER_B,
            pool=POOL_USDC_WETH_V3,
            token_in=WETH,
            token_out=USDC,
            amount_in=5 * 10**16,
            amount_out=151 * 10**6,
            gas_price_wei=20_000_000_000,
            gas_used=128_000,
        ),
    ]


def run_demo_scan() -> List[Event]:
    sink = StdoutSink()
    swaps = fixture_swaps()
    result = classify_block(swaps, block_number=21000000)
    for ev in result.events:
        score = score_event(ev)
        sink.emit(ev, score)
    return result.events

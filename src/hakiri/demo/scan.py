"""demo scan: produces a small batch of synthetic mev events.

used for screencasts and offline tests. the fixtures are intentionally
hand-rolled (not real chain data) so nothing here defames real wallets.
"""

from __future__ import annotations

from typing import List

from hakiri.core.classify import classify_slot
from hakiri.core.score import score_event
from hakiri.core.types import Event, SwapTx
from hakiri.output.stdout import StdoutSink

SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
POOL_SOL_USDC = "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"
SEARCHER_A = "JTOArByrMvDPfH8XgbQDbbYxWh5XEW1Bkau3jDXRcLg"
SEARCHER_B = "Pump1NSXgGAa84iMJBmF1zFxWv7Y5GgqujRkDbTcdT4"
VICTIM = "VicT1mw411111111111111111111111111111111111"


def fixture_swaps() -> List[SwapTx]:
    """canonical sandwich pattern + a backrun + a noise tx."""
    return [
        SwapTx(
            signature="Sigaa01" + "1" * 81,
            slot=287000000,
            tx_index=0,
            sender=SEARCHER_A,
            pool=POOL_SOL_USDC,
            token_in=SOL,
            token_out=USDC,
            amount_in=8 * 10**9,
            amount_out=24_000 * 10**6,
            compute_unit_price=50_000,
            compute_units=140_000,
            jito_tip_lamports=12 * 10**6,
        ),
        SwapTx(
            signature="Sigbb02" + "2" * 81,
            slot=287000000,
            tx_index=1,
            sender=VICTIM,
            pool=POOL_SOL_USDC,
            token_in=SOL,
            token_out=USDC,
            amount_in=2 * 10**9,
            amount_out=5_950 * 10**6,
            compute_unit_price=18_000,
            compute_units=160_000,
        ),
        SwapTx(
            signature="Sigcc03" + "3" * 81,
            slot=287000000,
            tx_index=2,
            sender=SEARCHER_A,
            pool=POOL_SOL_USDC,
            token_in=USDC,
            token_out=SOL,
            amount_in=24_500 * 10**6,
            amount_out=8_300_000_000,
            compute_unit_price=49_000,
            compute_units=145_000,
            jito_tip_lamports=8 * 10**6,
        ),
        SwapTx(
            signature="Sigdd04" + "4" * 81,
            slot=287000000,
            tx_index=3,
            sender="Noise111111111111111111111111111111111111111",
            pool=POOL_SOL_USDC,
            token_in=SOL,
            token_out=USDC,
            amount_in=1 * 10**8,
            amount_out=305 * 10**6,
            compute_unit_price=20_000,
            compute_units=120_000,
        ),
        SwapTx(
            signature="Sigee05" + "5" * 81,
            slot=287000000,
            tx_index=4,
            sender=SEARCHER_B,
            pool=POOL_SOL_USDC,
            token_in=SOL,
            token_out=USDC,
            amount_in=5 * 10**7,
            amount_out=151 * 10**6,
            compute_unit_price=20_000,
            compute_units=128_000,
        ),
    ]


def run_demo_scan() -> List[Event]:
    sink = StdoutSink()
    swaps = fixture_swaps()
    result = classify_slot(swaps, slot=287000000)
    for ev in result.events:
        score = score_event(ev)
        sink.emit(ev, score)
    return result.events

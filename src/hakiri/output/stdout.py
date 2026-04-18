"""human-readable terminal sink. uses rich for color + alignment."""

from __future__ import annotations

from typing import Optional

from rich.console import Console
from rich.table import Table

from hakiri.core.score import Score
from hakiri.core.types import Event


class StdoutSink:
    """pretty-prints one event per call. one row per victim."""

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console = console or Console()

    def emit(self, event: Event, score: Score) -> None:
        title = (
            f"[bold]{event.kind.value.upper()}[/bold]  "
            f"block {event.block_number}  "
            f"verdict={score.verdict.value} "
            f"conf={score.confidence:.2f}"
        )
        self.console.print(title)

        if event.builder:
            self.console.print(f"  builder:  {event.builder}")
        if event.searcher:
            self.console.print(f"  searcher: {event.searcher}")
        if event.coinbase_transfer_wei > 0:
            eth = event.coinbase_transfer_wei / 1e18
            self.console.print(f"  coinbase: {eth:.6f} eth")

        if event.victims:
            t = Table(show_header=True, header_style="dim")
            t.add_column("victim_tx")
            t.add_column("sender")
            t.add_column("loss_eth", justify="right")
            for v in event.victims:
                t.add_row(v.tx_hash, v.sender, f"{v.loss_eth:.6f}")
            self.console.print(t)

        if event.notes:
            self.console.print(f"  rules:    {', '.join(event.notes)}")
        self.console.print()

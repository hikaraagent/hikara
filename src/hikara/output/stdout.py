"""human-readable terminal sink. uses rich for color + alignment."""

from __future__ import annotations

from typing import Optional

from rich.console import Console
from rich.table import Table

from hikara.core.score import Score
from hikara.core.types import Event


class StdoutSink:
    """pretty-prints one event per call. one row per victim."""

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console = console or Console()

    def emit(self, event: Event, score: Score) -> None:
        title = (
            f"[bold]{event.kind.value.upper()}[/bold]  "
            f"slot {event.slot}  "
            f"verdict={score.verdict.value} "
            f"conf={score.confidence:.2f}"
        )
        self.console.print(title)

        if event.leader:
            self.console.print(f"  leader:   {event.leader}")
        if event.searcher:
            self.console.print(f"  searcher: {event.searcher}")
        if event.jito_tip_lamports > 0:
            sol = event.jito_tip_lamports / 1e9
            self.console.print(f"  jito_tip: {sol:.6f} sol")

        if event.victims:
            t = Table(show_header=True, header_style="dim")
            t.add_column("victim_sig")
            t.add_column("sender")
            t.add_column("loss_sol", justify="right")
            for v in event.victims:
                t.add_row(v.signature, v.sender, f"{v.loss_sol:.6f}")
            self.console.print(t)

        if event.notes:
            self.console.print(f"  rules:    {', '.join(event.notes)}")
        self.console.print()

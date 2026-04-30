"""replay a single recorded slot from the fixtures dir.

stub. a future minor will load fixtures from `tests/fixtures/slots/<n>.json`
and run them through the full pipeline. for now this command exists so the
cli has a third demo path.

TODO(luka): wire fixture loader. tracking issue: #31.
"""

from __future__ import annotations

from rich.console import Console


def run_demo_replay(slot_id: str) -> None:
    c = Console()
    c.print(f"[dim]replay stub. slot_id={slot_id}.[/dim]")
    c.print("future minor: will load tests/fixtures/slots/<id>.json and re-run pipeline.")

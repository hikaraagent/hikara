"""replay a single recorded block from the fixtures dir.

stub. v0.2 will load fixtures from `tests/fixtures/blocks/<n>.json` and
run them through the full pipeline. for now this command exists so the
cli has a third demo path.

TODO(senri): wire fixture loader. tracking issue: #31.
"""

from __future__ import annotations

from rich.console import Console


def run_demo_replay(block_id: str) -> None:
    c = Console()
    c.print(f"[dim]replay stub. block_id={block_id}.[/dim]")
    c.print("v0.2: will load tests/fixtures/blocks/<id>.json and re-run pipeline.")

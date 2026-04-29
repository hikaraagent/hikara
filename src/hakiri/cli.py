"""hakiri command-line interface.

four command groups:
  scan        run live scanner against configured rpc.
  investigate dive into a single tx_hash or block.
  demo        scripted offline demos.
  version     print version + build info.
"""

from __future__ import annotations

import typer
from rich.console import Console

from hakiri import __version__
from hakiri.config import load
from hakiri.demo.investigate import run_demo_investigate
from hakiri.demo.replay import run_demo_replay
from hakiri.demo.scan import run_demo_scan

app = typer.Typer(
    name="hakiri",
    add_completion=False,
    help="ethereum mev forensics agent. read-only by design.",
    no_args_is_help=True,
)

demo_app = typer.Typer(
    name="demo", help="scripted offline demos. zero network.", no_args_is_help=True
)
app.add_typer(demo_app, name="demo")


@app.command()
def version() -> None:
    """print version + build info."""
    console = Console()
    settings = load()
    console.print(f"hakiri {__version__}")
    console.print(f"  trace_mode: {settings.trace_mode}")
    console.print(f"  rpc:        {'set' if settings.has_rpc else 'unset'}")
    console.print(f"  ai:         {'set' if settings.has_ai else 'unset'}")
    console.print(f"  sink:       {settings.sink}")


@app.command()
def scan(
    once: bool = typer.Option(
        False, "--once", help="exit after first block (smoke test)."
    ),
) -> None:
    """run the live scanner. requires HAKIRI_WS_URL or HAKIRI_HTTP_URL."""
    settings = load()
    console = Console()
    if not settings.has_rpc:
        console.print(
            "[yellow]no rpc configured. set HAKIRI_WS_URL or HAKIRI_HTTP_URL.[/yellow]"
        )
        console.print("falling back to demo scan.")
        run_demo_scan()
        return
    console.print("[yellow]live scan stub. v0.2 will wire ingest-rs.[/yellow]")
    console.print(f"would connect to: {settings.ws_url or settings.http_url}")
    console.print(f"once={once}")


@app.command()
def investigate(
    target: str = typer.Argument(..., help="tx hash or block number."),
) -> None:
    """investigate a tx hash or block number."""
    settings = load()
    console = Console()
    if not settings.has_rpc:
        console.print(
            f"[yellow]no rpc. running offline demo for target={target}.[/yellow]"
        )
        run_demo_investigate()
        return
    console.print(f"[yellow]investigate stub. target={target}.[/yellow]")


@demo_app.command("scan")
def demo_scan() -> None:
    """canned scan of a synthetic block. emits to stdout."""
    run_demo_scan()


@demo_app.command("investigate")
def demo_investigate() -> None:
    """walk the full pipeline on a synthetic sandwich block."""
    run_demo_investigate()


@demo_app.command("replay")
def demo_replay(
    block_id: str = typer.Argument(..., help="fixture block id."),
) -> None:
    """replay a recorded block fixture."""
    run_demo_replay(block_id)


if __name__ == "__main__":
    app()

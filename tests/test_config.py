"""tests for hakiri.config."""

from __future__ import annotations

import os

from hakiri.config import Settings, load


def test_defaults(monkeypatch) -> None:
    for k in list(os.environ):
        if k.startswith("HAKIRI_") or k == "ANTHROPIC_API_KEY":
            monkeypatch.delenv(k, raising=False)
    s = Settings()
    assert s.trace_mode == "getblock"
    assert s.sink == "stdout"
    assert not s.has_rpc
    assert not s.has_stream
    assert not s.has_ai


def test_env_loads_rpc(monkeypatch) -> None:
    monkeypatch.setenv("HAKIRI_RPC_HTTP_URL", "https://api.mainnet-beta.solana.com")
    s = load()
    assert s.has_rpc is True


def test_env_loads_stream(monkeypatch) -> None:
    monkeypatch.setenv(
        "HAKIRI_GEYSER_GRPC_URL", "https://yellowstone.example.com:10000"
    )
    s = load()
    assert s.has_stream is True

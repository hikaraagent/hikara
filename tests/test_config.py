"""tests for hakiri.config."""

from __future__ import annotations

import os

from hakiri.config import Settings, load


def test_defaults(monkeypatch) -> None:
    for k in list(os.environ):
        if k.startswith("HAKIRI_") or k == "ANTHROPIC_API_KEY":
            monkeypatch.delenv(k, raising=False)
    s = Settings()
    assert s.trace_mode == "rpc"
    assert s.sink == "stdout"
    assert not s.has_rpc
    assert not s.has_ai


def test_env_loads_rpc(monkeypatch) -> None:
    monkeypatch.setenv("HAKIRI_HTTP_URL", "https://example.org")
    s = load()
    assert s.has_rpc is True

"""runtime configuration. reads from env. nothing required to demo."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """environment-driven config. all keys optional. demo mode runs without any."""

    model_config = SettingsConfigDict(
        env_prefix="HAKIRI_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ws_url: Optional[str] = None
    http_url: Optional[str] = None

    relay_urls: List[str] = Field(
        default_factory=lambda: [
            "https://relay.flashbots.net",
            "https://relay.ultrasoundmoney.org",
        ]
    )

    trace_mode: Literal["debug", "parity", "rpc"] = "rpc"

    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    ai_model: str = "claude-haiku-4-5-20251001"

    sink: Literal["stdout", "jsonl", "webhook", "all"] = "stdout"
    jsonl_path: str = "./out/hakiri.jsonl"
    webhook_url: Optional[str] = None

    backfill_blocks: int = 0
    log_level: Literal["debug", "info", "warning", "error"] = "info"

    @property
    def has_rpc(self) -> bool:
        return bool(self.http_url) or bool(self.ws_url)

    @property
    def has_ai(self) -> bool:
        return bool(self.anthropic_api_key)


def load() -> Settings:
    """load and return settings. cached at the call site if needed."""
    return Settings()

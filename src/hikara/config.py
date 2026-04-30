"""runtime configuration. reads from env. nothing required to demo."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """environment-driven config. all keys optional. demo mode runs without any."""

    model_config = SettingsConfigDict(
        env_prefix="HIKARA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    rpc_http_url: Optional[str] = None
    rpc_ws_url: Optional[str] = None

    geyser_grpc_url: Optional[str] = None
    shredstream_url: Optional[str] = None
    jito_block_engine_url: str = "https://mainnet.block-engine.jito.wtf"

    trace_mode: Literal["getblock", "geyser", "shredstream"] = "getblock"

    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    ai_model: str = "claude-haiku-4-5-20251001"

    sink: Literal["stdout", "jsonl", "webhook", "all"] = "stdout"
    jsonl_path: str = "./out/hikara.jsonl"
    webhook_url: Optional[str] = None

    backfill_slots: int = 0
    log_level: Literal["debug", "info", "warning", "error"] = "info"

    @property
    def has_rpc(self) -> bool:
        return bool(self.rpc_http_url) or bool(self.rpc_ws_url)

    @property
    def has_stream(self) -> bool:
        return bool(self.geyser_grpc_url) or bool(self.shredstream_url)

    @property
    def has_ai(self) -> bool:
        return bool(self.anthropic_api_key)


def load() -> Settings:
    """load and return settings. cached at the call site if needed."""
    return Settings()

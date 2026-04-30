"""output sinks. take a scored event and emit it somewhere."""

from hikara.output.jsonl import JsonlSink
from hikara.output.stdout import StdoutSink
from hikara.output.webhook import WebhookSink

__all__ = ["JsonlSink", "StdoutSink", "WebhookSink"]

"""output sinks. take a scored event and emit it somewhere."""

from hakiri.output.jsonl import JsonlSink
from hakiri.output.stdout import StdoutSink
from hakiri.output.webhook import WebhookSink

__all__ = ["JsonlSink", "StdoutSink", "WebhookSink"]

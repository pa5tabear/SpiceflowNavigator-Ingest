import asyncio
from typing import Any


class QueueManager:
    """Container for asynchronous workflow queues."""

    def __init__(self) -> None:
        self.discovery: asyncio.Queue[Any] = asyncio.Queue()
        self.processing: asyncio.Queue[Any] = asyncio.Queue()
        self.assembly: asyncio.Queue[Any] = asyncio.Queue()
        self.delivery: asyncio.Queue[Any] = asyncio.Queue()

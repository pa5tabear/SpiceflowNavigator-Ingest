from __future__ import annotations

from pathlib import Path
from typing import Optional

from .queue_manager import QueueManager
from audio.chunker import AudioChunker


class WorkflowOrchestrator:
    """Basic orchestrator that moves items through the queues."""

    def __init__(self, queues: QueueManager | None = None, chunker: Optional[AudioChunker] = None) -> None:
        self.queues = queues or QueueManager()
        self.chunker = chunker

    async def process_once(self) -> None:
        """Move one item through all pipeline stages."""
        item = await self.queues.discovery.get()
        if self.chunker and isinstance(item, str):
            # treat the item as a path to an audio file
            await self.chunker.chunk(Path(item), Path(Path(item).parent))
        await self.queues.processing.put(f"processed:{item}")
        item = await self.queues.processing.get()
        await self.queues.assembly.put(f"assembled:{item}")
        item = await self.queues.assembly.get()
        await self.queues.delivery.put(f"delivered:{item}")

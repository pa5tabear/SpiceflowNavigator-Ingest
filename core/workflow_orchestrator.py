from __future__ import annotations

from .queue_manager import QueueManager


class WorkflowOrchestrator:
    """Basic orchestrator that moves items through the queues."""

    def __init__(self, queues: QueueManager | None = None) -> None:
        self.queues = queues or QueueManager()

    async def process_once(self) -> None:
        """Move one item through all pipeline stages."""
        item = await self.queues.discovery.get()
        await self.queues.processing.put(f"processed:{item}")
        item = await self.queues.processing.get()
        await self.queues.assembly.put(f"assembled:{item}")
        item = await self.queues.assembly.get()
        await self.queues.delivery.put(f"delivered:{item}")

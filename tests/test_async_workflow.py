import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.queue_manager import QueueManager
from core.workflow_orchestrator import WorkflowOrchestrator


def test_queue_manager_operations():
    qm = QueueManager()

    async def run():
        await qm.discovery.put("a")
        return await qm.discovery.get()

    result = asyncio.run(run())
    assert result == "a"


def test_orchestrator_passes_item():
    qm = QueueManager()
    orch = WorkflowOrchestrator(qm)

    async def run():
        await qm.discovery.put("item")
        await orch.process_once()
        return await qm.delivery.get()

    result = asyncio.run(run())
    assert result == "delivered:assembled:processed:item"

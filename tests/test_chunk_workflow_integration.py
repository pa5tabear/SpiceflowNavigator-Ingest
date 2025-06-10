import asyncio
import sys
from pathlib import Path
import types

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.queue_manager import QueueManager
from core.workflow_orchestrator import WorkflowOrchestrator
from audio.chunker import AudioChunker


class DummyChunker(AudioChunker):
    def __init__(self):
        super().__init__()
        self.called_with: list[Path] = []

    async def chunk(self, source: Path, dest_dir: Path):
        self.called_with.append(source)
        return []


def test_chunk_workflow_integration(monkeypatch, tmp_path):
    qm = QueueManager()
    chunker = DummyChunker()
    orch = WorkflowOrchestrator(qm, chunker=chunker)

    async def run():
        await qm.discovery.put(str(tmp_path / "a.mp3"))
        await orch.process_once()
        return await qm.delivery.get()

    result = asyncio.run(run())
    assert result == f"delivered:assembled:processed:{tmp_path / 'a.mp3'}"
    assert chunker.called_with

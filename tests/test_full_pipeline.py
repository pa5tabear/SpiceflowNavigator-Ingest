import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.queue_manager import QueueManager
from core.workflow_orchestrator import WorkflowOrchestrator
from core.transcript_assembler import TranscriptAssembler, TranscriptChunk
from audio.chunker import ChunkMetadata
from audio.file_manager import TempFileManager


class DummyDownloader:
    async def download(self, url: str, dest: Path) -> Path:
        dest.write_text("audio")
        return dest


class DummyValidator:
    async def validate(self, path: Path):
        return {"duration": 1.0}


class DummyChunker:
    async def chunk(self, source: Path, dest: Path):
        return [
            ChunkMetadata(0, 0.0, 1.0, dest / "c0.mp3", source),
            ChunkMetadata(1, 1.0, 2.0, dest / "c1.mp3", source),
        ]


class DummyTranscriber:
    async def transcribe(self, path: str, stream: bool = False) -> str:
        return "hello" if "c0" in path else "world"


def test_full_pipeline_integration(tmp_path):
    qm = QueueManager()
    fm = TempFileManager()
    orch = WorkflowOrchestrator(
        qm,
        downloader=DummyDownloader(),
        validator=DummyValidator(),
        chunker=DummyChunker(),
        transcriber=DummyTranscriber(),
        assembler=TranscriptAssembler(),
        file_manager=fm,
    )

    async def run():
        await qm.discovery.put("http://audio")
        await orch.process_once()
        return await qm.delivery.get()

    result = asyncio.run(run())
    assert result["text"] == "hello world"


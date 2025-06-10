from __future__ import annotations

from pathlib import Path
from typing import Optional, List

from .queue_manager import QueueManager
from audio.chunker import AudioChunker
from audio.file_manager import TempFileManager
from audio.downloader import AudioDownloader
from audio.validator import AudioValidator
from runpod_client import RunPodClient
from .transcript_assembler import TranscriptAssembler, TranscriptChunk


class WorkflowOrchestrator:
    """Basic orchestrator that moves items through the queues."""

    def __init__(
        self,
        queues: QueueManager | None = None,
        *,
        downloader: Optional[AudioDownloader] = None,
        validator: Optional[AudioValidator] = None,
        chunker: Optional[AudioChunker] = None,
        transcriber: Optional[RunPodClient] = None,
        assembler: Optional[TranscriptAssembler] = None,
        file_manager: Optional[TempFileManager] = None,
    ) -> None:
        self.queues = queues or QueueManager()
        self.downloader = downloader
        self.validator = validator
        self.chunker = chunker
        self.transcriber = transcriber
        self.assembler = assembler
        self.file_manager = file_manager or TempFileManager()

    async def process_once(self) -> None:
        """Move one item through all pipeline stages."""
        item = await self.queues.discovery.get()

        if not (self.transcriber and self.assembler):
            if self.chunker and isinstance(item, (str, Path)):
                path_obj = Path(item)
                await self.chunker.chunk(path_obj, path_obj.parent)
            await self.queues.processing.put(f"processed:{item}")
            item = await self.queues.processing.get()
            await self.queues.assembly.put(f"assembled:{item}")
            item = await self.queues.assembly.get()
            await self.queues.delivery.put(f"delivered:{item}")
            return

        # Optional downloader stage for URLs
        if self.downloader and isinstance(item, str) and item.startswith("http"):
            path = self.file_manager.create(".mp3")
            item = await self.downloader.download(item, path)

        await self.queues.processing.put(item)
        item = await self.queues.processing.get()

        # Validation and chunking
        path_obj = Path(item) if isinstance(item, (str, Path)) else None
        if self.validator and path_obj:
            await self.validator.validate(path_obj)
        chunks = []
        if self.chunker and path_obj:
            chunks = await self.chunker.chunk(path_obj, path_obj.parent)

        await self.queues.assembly.put(chunks or item)
        item = await self.queues.assembly.get()

        # Transcription + assembly
        if isinstance(item, list) and self.transcriber and self.assembler:
            results: List[TranscriptChunk] = []
            for ch in item:
                text = await self.transcriber.transcribe(str(ch.path))
                results.append(
                    TranscriptChunk(
                        index=ch.index,
                        start=ch.start,
                        end=ch.end,
                        text=text,
                        word_timestamps=[],
                    )
                )
            assembled = self.assembler.assemble(results)
            await self.queues.delivery.put(assembled)
        else:
            await self.queues.delivery.put(f"delivered:{item}")

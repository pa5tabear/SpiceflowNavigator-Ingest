from __future__ import annotations

import asyncio
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ChunkMetadata:
    index: int
    start: float
    end: float
    path: Path
    source: Path


class AudioChunker:
    """Simple ffmpeg-based audio chunker."""

    def __init__(self, min_seconds: int = 300, max_seconds: int = 900) -> None:
        self.min_seconds = min_seconds
        self.max_seconds = max_seconds

    async def chunk(self, source: Path, dest_dir: Path) -> List[ChunkMetadata]:
        return await asyncio.to_thread(self._chunk_sync, source, dest_dir)

    def _chunk_sync(self, source: Path, dest_dir: Path) -> List[ChunkMetadata]:
        duration = self._duration(source)
        chunk_size = max(self.min_seconds, min(self.max_seconds, 600))
        dest_dir.mkdir(parents=True, exist_ok=True)
        chunks = []
        start = 0.0
        index = 0
        while start < duration:
            end = min(start + chunk_size, duration)
            out = dest_dir / f"{source.stem}_chunk{index}{source.suffix}"
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                str(source),
                "-ss",
                str(start),
                "-t",
                str(end - start),
                "-acodec",
                "copy",
                str(out),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            chunks.append(ChunkMetadata(index=index, start=start, end=end, path=out, source=source))
            index += 1
            start = end
        return chunks

    def _duration(self, path: Path) -> float:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip() or 0.0)

    async def reassemble(self, chunks: List[ChunkMetadata], output: Path) -> Path:
        await asyncio.to_thread(self._reassemble_sync, chunks, output)
        return output

    def _reassemble_sync(self, chunks: List[ChunkMetadata], output: Path) -> None:
        list_file = output.with_suffix(".txt")
        with open(list_file, "w") as f:
            for chunk in chunks:
                f.write(f"file '{chunk.path}'\n")
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-acodec",
            "copy",
            str(output),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        list_file.unlink(missing_ok=True)

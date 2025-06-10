from __future__ import annotations

import asyncio
from pathlib import Path
import requests


class AudioDownloader:
    """Asynchronously download audio files with concurrency limits."""

    def __init__(self, max_concurrent: int = 3, temp_dir: Path | None = None) -> None:
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.temp_dir = Path(temp_dir or Path("temp_audio"))
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self._files: list[Path] = []

    @property
    def files(self) -> list[Path]:
        return list(self._files)

    async def download(self, url: str, *, filename: str | None = None) -> Path:
        """Download a single URL to the temp directory."""
        name = filename or Path(url.split("?")[0]).name or "audio"
        path = self.temp_dir / name
        async with self.semaphore:
            await asyncio.to_thread(self._stream_download, url, path)
        self._files.append(path)
        return path

    def _stream_download(self, url: str, path: Path) -> None:
        with requests.get(url, timeout=10, stream=True) as resp:
            resp.raise_for_status()
            with open(path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

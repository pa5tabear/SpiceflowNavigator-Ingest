from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Iterable
import requests


class AudioDownloader:
    """Asynchronously download audio files with concurrency limits."""

    def __init__(self, concurrency: int = 3) -> None:
        self.semaphore = asyncio.Semaphore(concurrency)

    async def download(self, url: str, dest: Path) -> Path:
        """Download a single file to the given destination."""
        async with self.semaphore:
            await asyncio.to_thread(self._download_sync, url, dest)
            return dest

    async def download_many(self, tasks: Iterable[tuple[str, Path]]) -> list[Path]:
        """Download multiple files concurrently."""
        coros = [self.download(url, path) for url, path in tasks]
        return await asyncio.gather(*coros)

    def _download_sync(self, url: str, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

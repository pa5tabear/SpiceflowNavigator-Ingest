from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Iterable, Tuple
import requests


class AudioDownloader:
    """Asynchronously download audio files with concurrency limits."""

    def __init__(self, concurrency: int = 3) -> None:
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)
        self._queue: asyncio.Queue[Tuple[str, Path, asyncio.Future[Path]]] = asyncio.Queue()
        self._started = False
        self._worker: asyncio.Task | None = None

    async def _ensure_worker(self) -> None:
        if not self._started:
            self._started = True
            self._worker = asyncio.create_task(self._worker_loop())

    async def _worker_loop(self) -> None:
        while True:
            url, dest, fut = await self._queue.get()
            asyncio.create_task(self._start_download(url, dest, fut))

    async def _start_download(self, url: str, dest: Path, fut: asyncio.Future[Path]) -> None:
        async with self.semaphore:
            try:
                await asyncio.to_thread(self._download_sync, url, dest)
                fut.set_result(dest)
            except Exception as exc:  # pragma: no cover - sanity
                fut.set_exception(exc)

    async def download(self, url: str, dest: Path) -> Path:
        """Download a single file to the given destination."""
        await self._ensure_worker()
        loop = asyncio.get_event_loop()
        fut: asyncio.Future[Path] = loop.create_future()
        await self._queue.put((url, dest, fut))
        return await fut

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

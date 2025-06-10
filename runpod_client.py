"""Asynchronous RunPod client with environment-backed configuration."""

from __future__ import annotations

import asyncio
from typing import Optional

from auth.runpod_client import RunPodClient as _SyncRunPodClient, Client
from config.environment import Environment


class RunPodClient(_SyncRunPodClient):
    """Async wrapper that defers to the synchronous client in a thread."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        *,
        api_key: Optional[str] = None,
        timeout: int = 300,
    ) -> None:
        env = Environment.load()
        super().__init__(endpoint or env.runpod_endpoint, timeout=timeout)
        self.api_key = api_key or env.runpod_api_key

    async def transcribe(self, file_path: str, *, stream: bool = False) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: _SyncRunPodClient.transcribe(self, file_path, stream=stream),
        )


__all__ = ["RunPodClient", "Client"]

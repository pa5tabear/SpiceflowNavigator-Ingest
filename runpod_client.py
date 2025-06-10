"""Asynchronous RunPod client with environment-backed configuration."""

from __future__ import annotations

import asyncio
from typing import Optional

import os
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
        if endpoint is None:
            env = Environment.load()
            endpoint = env.runpod_endpoint
            api_key = api_key or env.runpod_api_key
        else:
            if api_key is None:
                api_key = os.getenv("RUNPOD_API_KEY")

        super().__init__(endpoint, timeout=timeout)
        self.api_key = api_key

    async def transcribe(self, file_path: str, *, stream: bool = False) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: _SyncRunPodClient.transcribe(self, file_path, stream=stream),
        )


__all__ = ["RunPodClient", "Client"]

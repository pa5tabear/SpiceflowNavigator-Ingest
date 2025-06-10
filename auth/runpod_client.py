from __future__ import annotations

import os
from typing import Optional

try:
    from gradio_client import Client  # type: ignore
except Exception:  # pragma: no cover - optional dep

    class Client:  # type: ignore
        """Fallback client if gradio_client is unavailable."""

        def __init__(self, *args, **kwargs) -> None:  # pragma: no cover
            raise ImportError("gradio_client is required")


class RunPodClient:
    """Authenticated client wrapper for RunPod endpoints."""

    def __init__(self, endpoint: Optional[str] = None, *, timeout: int = 300) -> None:
        self.endpoint = endpoint or os.getenv("RUNPOD_ENDPOINT")
        if not self.endpoint:
            raise ValueError("RUNPOD_ENDPOINT not set")
        self.client = Client(self.endpoint, timeout=timeout)

    def transcribe(self, file_path: str, *, stream: bool = False) -> str:
        """Submit a transcription job."""
        return self.client.predict(
            file_path,
            "Systran/faster-whisper-large-v3",
            "transcribe",
            0.0,
            stream=stream,
            api_name="/predict",
        )

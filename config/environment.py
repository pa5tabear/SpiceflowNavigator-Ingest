from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Environment:
    """Environment configuration loader."""

    runpod_endpoint: str
    runpod_api_key: str | None = None

    @classmethod
    def load(cls) -> "Environment":
        endpoint = os.getenv("RUNPOD_ENDPOINT")
        if not endpoint:
            raise ValueError("RUNPOD_ENDPOINT not set")
        api_key = os.getenv("RUNPOD_API_KEY")
        return cls(runpod_endpoint=endpoint, runpod_api_key=api_key)

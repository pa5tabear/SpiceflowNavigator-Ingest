from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any, Dict


class AudioValidator:
    """Validate audio files using ffprobe."""

    async def validate(self, path: Path) -> Dict[str, Any]:
        try:
            data = await asyncio.to_thread(self._probe, path)
        except subprocess.CalledProcessError as exc:  # pragma: no cover - safety
            raise ValueError("ffprobe failed") from exc
        return data

    def _probe(self, path: Path) -> Dict[str, Any]:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-of",
            "json",
            str(path),
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        info = json.loads(result.stdout)
        fmt = info.get("format", {})
        return {
            "format": fmt.get("format_name"),
            "duration": float(fmt.get("duration", 0.0)),
            "bitrate": int(fmt.get("bit_rate", 0)),
        }

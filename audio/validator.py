from __future__ import annotations

import json
import subprocess
from pathlib import Path


class AudioValidator:
    """Validate audio files using ffprobe."""

    def __init__(self, ffprobe_bin: str = "ffprobe") -> None:
        self.ffprobe_bin = ffprobe_bin

    def _probe(self, path: Path) -> dict:
        cmd = [
            self.ffprobe_bin,
            "-v",
            "error",
            "-show_entries",
            "format=duration,format_name,bit_rate",
            "-of",
            "json",
            str(path),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"ffprobe failed for {path}")
        return json.loads(proc.stdout).get("format", {})

    def validate(self, path: Path) -> dict:
        """Return metadata if file is valid, raise otherwise."""
        info = self._probe(path)
        if not info.get("format_name"):
            raise ValueError("Unknown format")
        duration = float(info.get("duration", 0))
        if duration <= 0:
            raise ValueError("Invalid duration")
        return info

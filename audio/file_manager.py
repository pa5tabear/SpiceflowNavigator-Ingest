from __future__ import annotations

import tempfile
import uuid
from pathlib import Path


class TempFileManager:
    """Manage temporary files for the pipeline."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.files: list[Path] = []

    def create(self, suffix: str = "") -> Path:
        path = self.root / f"{uuid.uuid4().hex}{suffix}"
        self.files.append(path)
        return path

    def cleanup(self) -> None:
        self._tmp.cleanup()

    def __enter__(self) -> "TempFileManager":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()

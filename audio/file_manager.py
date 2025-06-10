from __future__ import annotations

import tempfile
import shutil
from pathlib import Path


class TempFileManager:
    """Manage temporary files for the audio pipeline."""

    def __init__(self, *, prefix: str = "ingest_") -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
        self._files: list[Path] = []

    @property
    def directory(self) -> Path:
        return self.temp_dir

    def track(self, path: Path) -> None:
        if path not in self._files:
            self._files.append(path)

    def cleanup(self) -> None:
        for p in self._files:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass
        shutil.rmtree(self.temp_dir, ignore_errors=True)

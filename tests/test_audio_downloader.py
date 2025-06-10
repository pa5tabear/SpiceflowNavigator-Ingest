import asyncio
from pathlib import Path
import types

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio import AudioDownloader


class DummyResp:
    def __init__(self) -> None:
        self.chunks = [b"a", b"b"]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def raise_for_status(self) -> None:
        pass

    def iter_content(self, chunk_size: int = 8192):
        for c in self.chunks:
            yield c


def test_audio_downloader(monkeypatch, tmp_path):
    def fake_get(url, timeout=10, stream=True):
        return DummyResp()

    monkeypatch.setattr("requests.get", fake_get)

    dl = AudioDownloader(max_concurrent=1, temp_dir=tmp_path)

    async def run() -> bytes:
        path = await dl.download("http://example/a.mp3")
        return path.read_bytes()

    data = asyncio.run(run())
    assert data == b"ab"

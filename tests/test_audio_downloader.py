import asyncio
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio import AudioDownloader  # noqa: E402
from audio.file_manager import TempFileManager  # noqa: E402


def test_audio_downloader_respects_concurrency(monkeypatch):
    calls = []

    def fake_get(url, stream=False, timeout=10):
        calls.append(url)

        class Resp:
            def raise_for_status(self):
                pass

            def iter_content(self, chunk_size=8192):
                time.sleep(0.05)
                yield b"data"

        return Resp()

    monkeypatch.setattr("audio.downloader.requests.get", fake_get)

    async def run(limit):
        with TempFileManager() as fm:
            downloader = AudioDownloader(concurrency=limit)
            p1 = fm.create(".mp3")
            p2 = fm.create(".mp3")
            start = time.perf_counter()
            await asyncio.gather(
                downloader.download("http://a", p1),
                downloader.download("http://b", p2),
            )
            duration = time.perf_counter() - start
            return duration, p1.read_bytes(), p2.read_bytes()

    duration1, d1, d2 = asyncio.run(run(1))
    duration2, _, _ = asyncio.run(run(2))

    assert d1 == b"data"
    assert d2 == b"data"
    assert duration1 > duration2
    assert calls == ["http://a", "http://b", "http://a", "http://b"]

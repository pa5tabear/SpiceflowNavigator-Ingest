import sys
from pathlib import Path
import types
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio.chunker import AudioChunker, ChunkMetadata


def test_audio_chunker_splits(monkeypatch, tmp_path):
    src = tmp_path / "a.mp3"
    src.write_bytes(b"data")

    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        if "ffprobe" in cmd[0]:
            class R: stdout = "100"  # duration 100s
            return R()

    monkeypatch.setattr("audio.chunker.subprocess.run", fake_run)

    chunker = AudioChunker(min_seconds=30, max_seconds=60)
    chunks = asyncio.run(chunker.chunk(src, tmp_path))

    assert len(chunks) == 2
    assert isinstance(chunks[0], ChunkMetadata)
    assert calls


def test_audio_chunker_reassemble(monkeypatch, tmp_path):
    out = tmp_path / "out.mp3"
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return types.SimpleNamespace()

    monkeypatch.setattr("audio.chunker.subprocess.run", fake_run)

    chunker = AudioChunker()
    chunks = [
        ChunkMetadata(0, 0, 1, tmp_path / "c1.mp3", tmp_path / "src.mp3"),
        ChunkMetadata(1, 1, 2, tmp_path / "c2.mp3", tmp_path / "src.mp3"),
    ]
    asyncio.run(chunker.reassemble(chunks, out))

    assert out.with_suffix(".txt") not in tmp_path.iterdir()
    assert calls

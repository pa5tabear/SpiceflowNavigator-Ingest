import asyncio
import sys
import json
import subprocess
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio import AudioValidator  # noqa: E402


def test_audio_validator_parses_metadata(monkeypatch, tmp_path):
    fake_output = json.dumps({"format": {"format_name": "mp3", "duration": "1.23", "bit_rate": "64000"}})

    class Result:
        stdout = fake_output

    def fake_run(*args, **kwargs):
        return Result()

    monkeypatch.setattr("audio.validator.subprocess.run", fake_run)

    path = tmp_path / "a.mp3"
    path.write_bytes(b"data")
    validator = AudioValidator()
    data = asyncio.run(validator.validate(path))

    assert data["format"] == "mp3"
    assert data["duration"] == 1.23
    assert data["bitrate"] == 64000


def test_audio_validator_raises_on_failure(monkeypatch, tmp_path):
    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "ffprobe")

    monkeypatch.setattr("audio.validator.subprocess.run", fake_run)

    path = tmp_path / "a.mp3"
    path.write_bytes(b"data")
    validator = AudioValidator()

    with pytest.raises(ValueError):
        asyncio.run(validator.validate(path))

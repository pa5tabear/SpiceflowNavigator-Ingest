from pathlib import Path
import json
import types

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio import AudioValidator


def test_audio_validator(monkeypatch, tmp_path):
    dummy_json = json.dumps({"format": {"duration": "5.0", "format_name": "mp3", "bit_rate": "64000"}})

    def fake_run(cmd, capture_output=True, text=True):
        return types.SimpleNamespace(returncode=0, stdout=dummy_json)

    monkeypatch.setattr("subprocess.run", fake_run)

    file_path = tmp_path / "a.mp3"
    file_path.write_bytes(b"dummy")

    v = AudioValidator()
    info = v.validate(file_path)
    assert info["format_name"] == "mp3"
    assert float(info["duration"]) == 5.0

import importlib
import json
import sys
from pathlib import Path
import types

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def load_module():
    import chunk_and_transcribe as mod
    return importlib.reload(mod)


def common_setup(monkeypatch, tmp_path, ci=False, patch_paths=True):
    if ci:
        monkeypatch.setenv("CI", "true")
    else:
        monkeypatch.delenv("CI", raising=False)
    mod = load_module()

    xml = "<rss><channel><item><enclosure url='http://example.com/a.mp3'/></item></channel></rss>"

    def fake_get(url, timeout=10, stream=False):
        return types.SimpleNamespace(text=xml, raise_for_status=lambda: None)

    monkeypatch.setattr(mod.requests, "get", fake_get)

    audio_path = tmp_path / "clip.mp3"

    def fake_download(url, path):
        path.write_text("audio")

    monkeypatch.setattr(mod, "download_clip", fake_download)

    result_json = tmp_path / "out.json"
    if patch_paths:
        monkeypatch.setattr(mod, "OUTPUT_AUDIO", audio_path)
        monkeypatch.setattr(mod, "TRANSCRIPT_PATH", result_json)

    dummy_client = types.SimpleNamespace(transcribe=lambda p: "hi")
    monkeypatch.setattr(mod, "RunPodClient", lambda: dummy_client)

    return mod, result_json


def test_chunk_and_transcribe_default(monkeypatch, tmp_path):
    mod, result_json = common_setup(monkeypatch, tmp_path, ci=False)
    assert mod.CLIP_SECONDS == 600
    mod.main()
    data = json.loads(result_json.read_text())
    assert data["transcript"] == "hi"


def test_chunk_and_transcribe_ci(monkeypatch, tmp_path):
    mod, _ = common_setup(monkeypatch, tmp_path, ci=True, patch_paths=False)
    assert mod.CLIP_SECONDS == 30
    assert mod.TRANSCRIPT_PATH.name == "30s_clip.json"
    # now patch paths and client for execution
    result_json = tmp_path / "out.json"
    monkeypatch.setattr(mod, "OUTPUT_AUDIO", tmp_path / "clip.mp3")
    monkeypatch.setattr(mod, "TRANSCRIPT_PATH", result_json)
    dummy_client = types.SimpleNamespace(transcribe=lambda p: "hi")
    monkeypatch.setattr(mod, "RunPodClient", lambda: dummy_client)
    mod.main()
    data = json.loads(result_json.read_text())
    assert data["transcript"] == "hi"

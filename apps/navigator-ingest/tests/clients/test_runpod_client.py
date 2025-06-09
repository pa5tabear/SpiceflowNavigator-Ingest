import sys
from pathlib import Path
import pytest

# Add the libs directory to the path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "libs" / "common-utils"))

from runpod_client import RunPodClient


class DummyClient:
    def __init__(self, endpoint, timeout=300):
        self.endpoint = endpoint
        self.timeout = timeout
        self.calls = []

    def predict(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return "dummy-result"


def test_init_requires_endpoint(monkeypatch):
    monkeypatch.delenv("RUNPOD_ENDPOINT", raising=False)
    with pytest.raises(ValueError):
        RunPodClient()


def test_init_from_env(monkeypatch):
    dummy = DummyClient("http://api")
    monkeypatch.setenv("RUNPOD_ENDPOINT", "http://api")
    monkeypatch.setattr(
        "runpod_client.Client", lambda endpoint, timeout=300: dummy
    )
    client = RunPodClient()
    assert client.endpoint == "http://api"
    assert client.client is dummy


def test_transcribe_calls_predict(monkeypatch):
    dummy = DummyClient("http://api")
    monkeypatch.setattr(
        "runpod_client.Client", lambda endpoint, timeout=300: dummy
    )
    client = RunPodClient("http://api")
    result = client.transcribe("file.wav", stream=True)
    assert result == "dummy-result"
    assert dummy.calls == [
        (
            ("file.wav", "Systran/faster-whisper-large-v3", "transcribe", 0.0),
            {"stream": True, "api_name": "/predict"},
        )
    ]

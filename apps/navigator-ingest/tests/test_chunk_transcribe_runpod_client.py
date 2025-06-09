import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from spiceflow.clients.runpod_client import RunPodClient


class DummyClient:
    def __init__(self, endpoint, timeout=300):
        self.endpoint = endpoint
        self.timeout = timeout
        self.calls = []

    def predict(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return "ok"


def test_chunk_transcribe_runpod_client(monkeypatch):
    dummy = DummyClient("http://api")
    monkeypatch.setenv("RUNPOD_ENDPOINT", "http://api")
    monkeypatch.setattr(
        "spiceflow.clients.runpod_client.Client", lambda endpoint, timeout=300: dummy
    )
    client = RunPodClient()
    result = client.transcribe("file.wav", stream=True)
    assert result == "ok"
    assert dummy.calls

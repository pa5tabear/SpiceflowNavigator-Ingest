import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio import TempFileManager  # noqa: E402


def test_temp_file_manager_creates_and_cleans():
    with TempFileManager() as fm:
        path = fm.create(".tmp")
        path.write_text("hi")
        root = fm.root
        assert path.exists()
    assert not root.exists()

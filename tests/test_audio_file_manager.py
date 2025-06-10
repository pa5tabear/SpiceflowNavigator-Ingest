from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio import TempFileManager


def test_audio_file_manager_cleanup(tmp_path):
    mgr = TempFileManager(prefix="test_")
    file_path = mgr.directory / "x.txt"
    file_path.write_text("data")
    mgr.track(file_path)
    mgr.cleanup()
    assert not mgr.directory.exists()

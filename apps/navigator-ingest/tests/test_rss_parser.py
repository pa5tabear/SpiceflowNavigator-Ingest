import sys
from pathlib import Path

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rss_parser import RSSParser


def test_rss_parser_extracts_audio_urls():
    xml_path = Path(__file__).resolve().parents[3] / "libs" / "common-utils" / "fixtures" / "shift_key_rss.xml"
    xml_content = xml_path.read_text()

    parser = RSSParser()
    urls = parser.extract_audio_urls(xml_content)

    assert len(urls) == 70
    assert all(url.endswith(".mp3") for url in urls)

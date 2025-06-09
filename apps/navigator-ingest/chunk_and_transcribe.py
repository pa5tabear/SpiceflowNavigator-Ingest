import json
import os
from pathlib import Path
import subprocess
import requests
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "libs" / "common-utils"))

from rss_parser import RSSParser
from runpod_client import RunPodClient

FEED_URL = "https://feeds.acast.com/public/shows/65bac3af03341c00164bf93b"

CI_MODE = os.getenv("CI") == "true"
CLIP_SECONDS = 30 if CI_MODE else 600

OUTPUT_AUDIO = (
    Path("latest_shift_key_30s.mp3") if CI_MODE else Path("latest_shift_key_10m.mp3")
)
TRANSCRIPT_PATH = Path("30s_clip.json") if CI_MODE else Path("10m_clip.json")


def fetch_latest_episode_url() -> str:
    resp = requests.get(FEED_URL, timeout=10)
    resp.raise_for_status()
    parser = RSSParser()
    urls = parser.extract_audio_urls(resp.text)
    if not urls:
        raise RuntimeError("No audio URLs found")
    return urls[0]


def download_clip(url: str, path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        url,
        "-t",
        str(CLIP_SECONDS),
        "-acodec",
        "copy",
        str(path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def transcribe_clip(path: Path) -> str:
    client = RunPodClient()
    text = client.transcribe(str(path))
    TRANSCRIPT_PATH.write_text(json.dumps({"transcript": text}))
    return text


def main() -> None:
    url = fetch_latest_episode_url()
    download_clip(url, OUTPUT_AUDIO)
    transcribe_clip(OUTPUT_AUDIO)


if __name__ == "__main__":
    main()

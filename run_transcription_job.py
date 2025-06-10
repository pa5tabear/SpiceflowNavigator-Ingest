import os
import requests
import runpod
from .rss_parser import RSSParser
from libs.common_utils.config import load_feeds




def latest_episode_url(feed_url: str) -> str:
    resp = requests.get(feed_url, timeout=10)
    resp.raise_for_status()
    parser = RSSParser()
    urls = parser.extract_audio_urls(resp.text)
    if not urls:
        raise RuntimeError("No audio URLs found")
    return urls[0]


def main() -> None:
    feeds = load_feeds()
    if not feeds:
        raise RuntimeError("No feeds configured")
    feed_url = feeds[0]

    audio_url = latest_episode_url(feed_url)

    api_key = os.getenv("RUNPOD_API_KEY")
    if not api_key:
        raise RuntimeError("RUNPOD_API_KEY not set")
    runpod.api_key = api_key

    endpoint_env = os.getenv("RUNPOD_ENDPOINT")
    if not endpoint_env:
        raise RuntimeError("RUNPOD_ENDPOINT not set")
    if endpoint_env.startswith("http"):
        endpoint_id = endpoint_env.split("//", 1)[1].split(".")[0].split("-")[0]
    else:
        endpoint_id = endpoint_env

    endpoint = runpod.Endpoint(endpoint_id)
    job = endpoint.run({"url": audio_url})
    print(job.job_id)


if __name__ == "__main__":
    main()

import asyncio
import hashlib
from typing import Optional

import requests

from rss_parser import RSSParser
from core.queue_manager import QueueManager


class RSSMonitor:
    """Asynchronously poll an RSS feed and enqueue new content."""

    def __init__(self, feed_url: str, *, interval: float = 60.0, queues: Optional[QueueManager] = None) -> None:
        self.feed_url = feed_url
        self.interval = interval
        self.queues = queues or QueueManager()
        self.parser = RSSParser()
        self._seen: set[str] = set()

    async def fetch_feed(self) -> str:
        """Fetch the raw RSS feed XML asynchronously."""
        return await asyncio.to_thread(lambda: requests.get(self.feed_url, timeout=10).text)

    def _hash(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    async def poll_once(self) -> list[str]:
        """Poll the RSS feed once and queue any new URLs."""
        xml = await self.fetch_feed()
        urls = self.parser.extract_audio_urls(xml)
        new_urls = []
        for url in urls:
            h = self._hash(url)
            if h not in self._seen:
                self._seen.add(h)
                await self.queues.discovery.put(url)
                new_urls.append(url)
        return new_urls

    async def start(self) -> None:
        """Continuously poll based on the configured interval."""
        while True:
            await self.poll_once()
            await asyncio.sleep(self.interval)

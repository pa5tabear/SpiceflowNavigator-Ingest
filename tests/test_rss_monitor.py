import asyncio
from rss_monitor import RSSMonitor


def make_xml(urls: list[str]) -> str:
    items = ''.join(f"<item><enclosure url='{u}'/></item>" for u in urls)
    return f"<rss><channel>{items}</channel></rss>"


def test_poll_once_enqueues_new_urls(monkeypatch):
    xml = make_xml(["a.mp3", "b.mp3"])
    monitor = RSSMonitor("http://feed")

    async def dummy_fetch(self):
        return xml

    async def run():
        monkeypatch.setattr(RSSMonitor, "fetch_feed", dummy_fetch)
        await monitor.poll_once()
        assert await monitor.queues.discovery.get() == "a.mp3"
        assert await monitor.queues.discovery.get() == "b.mp3"

    asyncio.run(run())


def test_deduplication(monkeypatch):
    xml = make_xml(["a.mp3"])  # same item every poll
    monitor = RSSMonitor("http://feed")

    async def dummy_fetch(self):
        return xml

    async def run():
        monkeypatch.setattr(RSSMonitor, "fetch_feed", dummy_fetch)
        await monitor.poll_once()
        await monitor.poll_once()
        assert monitor.queues.discovery.qsize() == 1
        assert await monitor.queues.discovery.get() == "a.mp3"

    asyncio.run(run())

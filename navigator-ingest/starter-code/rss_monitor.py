"""
Enhanced RSS Feed Monitoring System
Real-time monitoring with intelligent change detection and configurable intervals.

This is STARTER CODE for Navigator-Ingest Feature 1: Real-Time RSS Feed Monitoring
"""

import asyncio
import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional
import logging

# Assuming CommonUtils submodule is available
from config import load_feeds, RSSFeed
from rss_parser import RSSParser  # Your existing RSS parser

@dataclass
class ContentFingerprint:
    """Unique identifier for RSS content to detect changes."""
    url: str
    title_hash: str
    content_hash: str
    pub_date: datetime
    
    @classmethod
    def from_entry(cls, entry: Dict) -> 'ContentFingerprint':
        """Create fingerprint from RSS entry."""
        url = entry.get('link', '')
        title = entry.get('title', '')
        content = entry.get('description', '') + entry.get('summary', '')
        
        title_hash = hashlib.sha256(title.encode()).hexdigest()[:12]
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        
        # Parse publication date
        pub_date = datetime.now()  # Fallback
        if 'published_parsed' in entry:
            pub_date = datetime(*entry['published_parsed'][:6])
            
        return cls(url=url, title_hash=title_hash, 
                  content_hash=content_hash, pub_date=pub_date)

@dataclass
class FeedMonitorConfig:
    """Configuration for monitoring a specific RSS feed."""
    feed: RSSFeed
    poll_interval: int = field(default=300)  # seconds
    max_retries: int = field(default=3)
    backoff_multiplier: float = field(default=2.0)
    last_check: Optional[datetime] = field(default=None)
    consecutive_failures: int = field(default=0)
    
    def __post_init__(self):
        # Calculate poll interval based on strategic importance
        # Higher importance = more frequent polling
        base_interval = 600  # 10 minutes
        importance_factor = max(1, self.feed.strategic_importance)
        self.poll_interval = max(60, base_interval // importance_factor)

class RSSMonitor:
    """Real-time RSS feed monitoring with intelligent change detection."""
    
    def __init__(self, state_file: Path = Path("rss_monitor_state.json")):
        self.parser = RSSParser()
        self.state_file = state_file
        self.feeds = load_feeds()
        self.monitor_configs = [FeedMonitorConfig(feed) for feed in self.feeds]
        self.seen_content: Set[str] = set()  # Content fingerprints
        self.logger = logging.getLogger(__name__)
        
        # Load previous state
        self._load_state()
    
    def _load_state(self):
        """Load monitoring state from disk."""
        if self.state_file.exists():
            # Implementation: Load seen_content and last_check times
            # This is a placeholder - implement JSON state persistence
            pass
    
    def _save_state(self):
        """Save monitoring state to disk."""
        # Implementation: Save seen_content and monitor states
        # This is a placeholder - implement JSON state persistence
        pass
    
    def _calculate_next_check(self, config: FeedMonitorConfig) -> datetime:
        """Calculate when to next check this feed."""
        if config.consecutive_failures > 0:
            # Exponential backoff for failed feeds
            backoff_seconds = config.poll_interval * (
                config.backoff_multiplier ** config.consecutive_failures
            )
            backoff_seconds = min(backoff_seconds, 3600)  # Max 1 hour
            return datetime.now() + timedelta(seconds=backoff_seconds)
        
        return datetime.now() + timedelta(seconds=config.poll_interval)
    
    async def _check_feed(self, config: FeedMonitorConfig) -> List[Dict]:
        """Check a single feed for new content."""
        try:
            # Parse the feed
            entries = await asyncio.to_thread(
                self.parser.parse_feed, config.feed.url
            )
            
            # Filter out content we've seen before
            new_entries = []
            for entry in entries:
                fingerprint = ContentFingerprint.from_entry(entry)
                fingerprint_str = f"{fingerprint.url}:{fingerprint.content_hash}"
                
                if fingerprint_str not in self.seen_content:
                    new_entries.append(entry)
                    self.seen_content.add(fingerprint_str)
                    self.logger.info(f"New content found: {entry.get('title', 'Unknown')}")
            
            # Reset failure count on success
            config.consecutive_failures = 0
            config.last_check = datetime.now()
            
            return new_entries
            
        except Exception as e:
            config.consecutive_failures += 1
            self.logger.error(f"Failed to check feed {config.feed.name}: {e}")
            
            if config.consecutive_failures >= config.max_retries:
                self.logger.warning(f"Feed {config.feed.name} exceeded max retries")
            
            return []
    
    async def _process_new_content(self, entries: List[Dict], feed: RSSFeed):
        """Process newly discovered content."""
        for entry in entries:
            self.logger.info(f"Processing: {entry.get('title', 'Unknown')} from {feed.name}")
            
            # Add strategic importance to entry
            entry['strategic_importance'] = feed.strategic_importance
            entry['source_feed'] = feed.name
            
            # TODO: Emit to processing pipeline
            # This would integrate with your existing transcription workflow
            # For example: await self.submit_to_transcription_queue(entry)
    
    async def monitor_feed(self, config: FeedMonitorConfig):
        """Monitor a single feed continuously."""
        while True:
            try:
                next_check = self._calculate_next_check(config)
                now = datetime.now()
                
                if now >= next_check:
                    self.logger.debug(f"Checking feed: {config.feed.name}")
                    new_entries = await self._check_feed(config)
                    
                    if new_entries:
                        await self._process_new_content(new_entries, config.feed)
                    
                    self._save_state()
                
                # Sleep for a short interval before checking again
                await asyncio.sleep(10)  # Check every 10 seconds if it's time
                
            except Exception as e:
                self.logger.error(f"Error in monitor loop for {config.feed.name}: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def start_monitoring(self):
        """Start monitoring all configured feeds."""
        self.logger.info(f"Starting RSS monitoring for {len(self.monitor_configs)} feeds")
        
        # Create monitoring tasks for all feeds
        tasks = [
            asyncio.create_task(self.monitor_feed(config))
            for config in self.monitor_configs
        ]
        
        try:
            # Run all monitoring tasks concurrently
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            self.logger.info("Shutting down RSS monitor...")
            self._save_state()
    
    def get_monitoring_status(self) -> Dict:
        """Get current monitoring status for all feeds."""
        status = {
            "feeds_monitored": len(self.monitor_configs),
            "total_content_seen": len(self.seen_content),
            "feeds": []
        }
        
        for config in self.monitor_configs:
            feed_status = {
                "name": config.feed.name,
                "url": config.feed.url,
                "strategic_importance": config.feed.strategic_importance,
                "poll_interval": config.poll_interval,
                "last_check": config.last_check.isoformat() if config.last_check else None,
                "consecutive_failures": config.consecutive_failures,
                "status": "healthy" if config.consecutive_failures == 0 else "degraded"
            }
            status["feeds"].append(feed_status)
        
        return status

# Example usage and testing
async def main():
    """Example usage of the RSS Monitor."""
    logging.basicConfig(level=logging.INFO)
    
    monitor = RSSMonitor()
    
    # Start monitoring (this runs indefinitely)
    await monitor.start_monitoring()

if __name__ == "__main__":
    # Example of how to run the monitor
    asyncio.run(main())

# NEXT STEPS for implementation:
# 1. Implement state persistence (JSON file or database)
# 2. Add integration with existing transcription pipeline
# 3. Add metrics collection for performance monitoring
# 4. Add configuration for custom polling intervals
# 5. Add health check endpoints for monitoring
# 6. Add graceful shutdown handling
# 7. Add batch processing capabilities for high-volume feeds 
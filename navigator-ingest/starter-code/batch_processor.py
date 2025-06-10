"""
Batch Processing Pipeline for Navigator-Ingest
Handles concurrent processing of multiple content items with job queuing.

This is STARTER CODE for Navigator-Ingest Feature 5: Distributed Processing Architecture
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
import logging
import uuid
import json

# Assuming CommonUtils submodule and existing modules
from runpod_client import RunPodClient

class JobStatus(Enum):
    """Job processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class ProcessingJob:
    """Represents a single content processing job."""
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content_url: str = ""
    content_type: str = ""  # "audio", "rss", "video", etc.
    source_feed: str = ""
    priority: int = 5  # 1-10, higher = more urgent
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict:
        """Convert job to dictionary for serialization."""
        return {
            "job_id": self.job_id,
            "content_url": self.content_url,
            "content_type": self.content_type,
            "source_feed": self.source_feed,
            "priority": self.priority,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProcessingJob':
        """Create job from dictionary."""
        job = cls()
        job.job_id = data["job_id"]
        job.content_url = data["content_url"]
        job.content_type = data["content_type"]
        job.source_feed = data["source_feed"]
        job.priority = data["priority"]
        job.status = JobStatus(data["status"])
        job.created_at = datetime.fromisoformat(data["created_at"])
        if data["started_at"]:
            job.started_at = datetime.fromisoformat(data["started_at"])
        if data["completed_at"]:
            job.completed_at = datetime.fromisoformat(data["completed_at"])
        job.result = data["result"]
        job.error_message = data["error_message"]
        job.retry_count = data["retry_count"]
        job.max_retries = data["max_retries"]
        return job

class JobQueue:
    """Priority job queue with persistence."""
    
    def __init__(self, queue_file: Path = Path("job_queue.json")):
        self.queue_file = queue_file
        self.jobs: List[ProcessingJob] = []
        self.logger = logging.getLogger(__name__)
        self._load_queue()
    
    def _load_queue(self):
        """Load job queue from disk."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                    self.jobs = [ProcessingJob.from_dict(job_data) for job_data in data]
                self.logger.info(f"Loaded {len(self.jobs)} jobs from queue")
            except Exception as e:
                self.logger.error(f"Failed to load job queue: {e}")
    
    def _save_queue(self):
        """Save job queue to disk."""
        try:
            with open(self.queue_file, 'w') as f:
                json.dump([job.to_dict() for job in self.jobs], f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save job queue: {e}")
    
    def add_job(self, job: ProcessingJob):
        """Add job to queue with priority sorting."""
        self.jobs.append(job)
        # Sort by priority (higher first) then by creation time
        self.jobs.sort(key=lambda j: (-j.priority, j.created_at))
        self._save_queue()
        self.logger.info(f"Added job {job.job_id} to queue (priority {job.priority})")
    
    def get_next_job(self) -> Optional[ProcessingJob]:
        """Get next pending job from queue."""
        for job in self.jobs:
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.PROCESSING
                job.started_at = datetime.now()
                self._save_queue()
                return job
        return None
    
    def complete_job(self, job_id: str, result: Dict):
        """Mark job as completed with result."""
        job = self._find_job(job_id)
        if job:
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()
            job.result = result
            self._save_queue()
            self.logger.info(f"Job {job_id} completed successfully")
    
    def fail_job(self, job_id: str, error_message: str):
        """Mark job as failed or retry if retries remain."""
        job = self._find_job(job_id)
        if job:
            job.retry_count += 1
            if job.retry_count <= job.max_retries:
                job.status = JobStatus.PENDING  # Retry
                job.started_at = None
                self.logger.warning(f"Job {job_id} failed, retrying ({job.retry_count}/{job.max_retries})")
            else:
                job.status = JobStatus.FAILED
                job.completed_at = datetime.now()
                job.error_message = error_message
                self.logger.error(f"Job {job_id} failed permanently: {error_message}")
            self._save_queue()
    
    def _find_job(self, job_id: str) -> Optional[ProcessingJob]:
        """Find job by ID."""
        return next((job for job in self.jobs if job.job_id == job_id), None)
    
    def get_queue_status(self) -> Dict:
        """Get current queue statistics."""
        status_counts = {}
        for status in JobStatus:
            status_counts[status.value] = sum(1 for job in self.jobs if job.status == status)
        
        return {
            "total_jobs": len(self.jobs),
            "by_status": status_counts,
            "oldest_pending": min(
                (job.created_at for job in self.jobs if job.status == JobStatus.PENDING),
                default=None
            )
        }

class BatchProcessor:
    """Distributed batch processor for content ingestion."""
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.job_queue: List[ProcessingJob] = []
        self.logger = logging.getLogger(__name__)
    
    async def submit_job(self, content_url: str, content_type: str) -> str:
        """Submit a new job for processing."""
        job = ProcessingJob(
            content_url=content_url,
            content_type=content_type
        )
        self.job_queue.append(job)
        self.logger.info(f"Submitted job {job.job_id}")
        return job.job_id
    
    async def process_job(self, job: ProcessingJob):
        """Process a single job."""
        try:
            job.status = JobStatus.PROCESSING
            
            if job.content_type == "audio":
                # Placeholder for audio processing
                result = {"transcript": "Sample transcript"}
            elif job.content_type == "rss":
                # Placeholder for RSS processing  
                result = {"items": 5}
            else:
                raise ValueError(f"Unknown content type: {job.content_type}")
            
            job.result = result
            job.status = JobStatus.COMPLETED
            self.logger.info(f"Completed job {job.job_id}")
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            self.logger.error(f"Failed job {job.job_id}: {e}")

# NEXT STEPS: Implement full worker pool, persistence, and integration

# Example usage
async def main():
    """Example usage of the batch processor."""
    logging.basicConfig(level=logging.INFO)
    
    processor = BatchProcessor(max_workers=2)
    
    # Submit some example jobs
    job1 = processor.submit_job(
        content_url="https://example.com/audio.mp3",
        content_type="audio",
        source_feed="tech_podcast",
        priority=8
    )
    
    job2 = processor.submit_job(
        content_url="https://example.com/feed.rss",
        content_type="rss",
        source_feed="news_feed",
        priority=5
    )
    
    print(f"Submitted jobs: {job1}, {job2}")
    print("Status:", processor.get_status())
    
    # Start processing (this runs indefinitely)
    try:
        await processor.start_processing()
    except KeyboardInterrupt:
        await processor.shutdown()

if __name__ == "__main__":
    asyncio.run(main())

# NEXT STEPS for implementation:
# 1. Integrate with existing RSS parser and transcription modules
# 2. Add health monitoring and metrics collection
# 3. Implement load balancing across multiple RunPod endpoints
# 4. Add job prioritization based on strategic importance
# 5. Add dead letter queue for permanently failed jobs
# 6. Add job scheduling and delayed execution
# 7. Add database persistence instead of JSON files
# 8. Add worker auto-scaling based on queue depth 
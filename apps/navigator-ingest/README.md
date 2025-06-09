# Navigator Ingest Agent

**Owner**: Agent 2 - RSS monitoring and transcription  
**Responsibility**: RSS monitoring, audio fetching, and Whisper transcription via RunPod

## Purpose
This agent handles all audio ingestion and transcription:
- Monitors RSS feeds for new episodes
- Downloads audio files from podcast URLs
- Submits audio to RunPod for Whisper transcription
- Stores transcripts and metadata

## API Contracts
- **Endpoints**: 
  - `POST /ingest?rss_id=...` - Trigger ingestion for RSS feed
  - `GET /transcript/{id}` - Retrieve transcript by ID
- **Output**: Transcript data with timestamps and metadata
- **Dependencies**: RunPod API, RSS feeds

## Development
```bash
# Run this agent
make dev-ingest

# Test this agent
pytest apps/navigator-ingest/tests/
``` 
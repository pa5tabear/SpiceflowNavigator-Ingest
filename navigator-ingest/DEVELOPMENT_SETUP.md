# 🛠️ Navigator-Ingest: Development Setup Guide

## 🚀 Quick Start (5 Minutes)

Get your Navigator-Ingest development environment running in 5 minutes:

```bash
# 1. Clone your independent repository with CommonUtils submodule
git clone --recursive https://github.com/pa5tabear/SpiceflowNavigator-Ingest.git
cd SpiceflowNavigator-Ingest

# 2. Install dependencies and CommonUtils
make install

# 3. Set required environment variables
export RUNPOD_ENDPOINT="https://your-runpod-endpoint.com"

# 4. Verify setup works
make test

# 5. Run a sample ingestion job
make dev
```

## 📋 Prerequisites

### Required Software
- **Python 3.9+** (Navigator-Ingest requires modern Python)
- **Git** with submodule support
- **Make** for development automation
- **pip** or **pipenv** for dependency management

### Optional but Recommended
- **Docker** (for isolated development)
- **VS Code** or **Cursor** (AI-optimized development)
- **RunPod Account** (for audio transcription)

## 🔧 Detailed Setup

### 1. Repository Setup

**Clone with Submodules:**
```bash
# Clone with CommonUtils submodule
git clone --recursive https://github.com/pa5tabear/SpiceflowNavigator-Ingest.git
cd SpiceflowNavigator-Ingest

# If you forgot --recursive, initialize submodules
git submodule update --init --recursive
```

**Verify Repository Structure:**
```bash
ls -la
# Should show: rss_parser.py, run_transcription_job.py, chunk_and_transcribe.py, common-utils/
```

### 2. Environment Configuration

**Required Environment Variables:**
```bash
# Add to your ~/.bashrc or ~/.zshrc
export RUNPOD_ENDPOINT="https://your-runpod-endpoint.com"

# Optional: For integration tests
export RUNPOD_API_KEY="your-api-key"

# Optional: Development settings
export PYTHONPATH="${PYTHONPATH}:${PWD}:${PWD}/common-utils"
```

**Create .env file (local development):**
```bash
# Create .env file for local development
cat > .env << EOF
RUNPOD_ENDPOINT=https://your-runpod-endpoint.com
RUNPOD_API_KEY=your-api-key-here
PYTHONPATH=.:./common-utils
EOF
```

### 3. Dependency Installation

**Using Make (Recommended):**
```bash
# Install all dependencies including CommonUtils
make install

# Verify installation
make test-deps
```

**Manual Installation:**
```bash
# Install main dependencies
pip install -r requirements.txt

# Install CommonUtils in development mode
cd common-utils
pip install -e .
cd ..
```

**Using Virtual Environment:**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
make install
```

## ⚡ Development Commands

### Essential Make Commands

```bash
# Development
make install        # Install dependencies + CommonUtils
make dev           # Run transcription job
make test          # Run full test suite
make clean         # Clean temporary files

# Testing
make test-unit     # Unit tests only
make test-integration  # Integration tests (requires RUNPOD_ENDPOINT)
make test-coverage # Test coverage report

# Code Quality
make lint          # Run linting (ruff)
make format        # Format code (ruff format)
make typecheck     # Type checking (mypy)

# CI/CD
make check-deps    # Verify no new dependencies
make check-coverage # Verify coverage thresholds
```

### Manual Commands

```bash
# Run specific components
python rss_parser.py                    # Parse RSS feeds
python run_transcription_job.py         # Full transcription pipeline
python chunk_and_transcribe.py          # Audio processing only

# Testing
pytest tests/ -v                        # Verbose test output
pytest -k test_rss_parser              # Run specific tests
pytest --cov=. --cov-report=html       # Coverage with HTML report

# Development server
python -m http.server 8000              # Serve test files locally
```

## 🧪 Testing Setup

### Test Categories

**Unit Tests (Fast, No External Dependencies):**
```bash
pytest tests/test_rss_parser.py
pytest tests/test_chunk_transcribe.py
```

**Integration Tests (Requires RunPod):**
```bash
# Set RUNPOD_ENDPOINT first
pytest tests/test_chunk_transcribe_runpod_client.py
```

**Mocked Tests (CommonUtils Integration):**
```bash
pytest tests/clients/test_runpod_client.py
```

### Test Data and Fixtures

**RSS Feed Fixtures:**
```bash
# Located in common-utils/fixtures/
ls common-utils/fixtures/
# Should show: mock_rss_feeds.xml, sample_audio.mp3, etc.
```

**Creating Test Data:**
```bash
# Add new RSS feed fixture
cat > common-utils/fixtures/test_feed.xml << EOF
<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <item>
      <title>Test Item</title>
      <link>https://example.com/audio.mp3</link>
      <description>Test description</description>
    </item>
  </channel>
</rss>
EOF
```

## 🐳 Docker Development (Optional)

**Dockerfile for Development:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e common-utils/

CMD ["python", "run_transcription_job.py"]
```

**Docker Compose for Development:**
```yaml
version: '3.8'
services:
  navigator-ingest:
    build: .
    environment:
      - RUNPOD_ENDPOINT=${RUNPOD_ENDPOINT}
    volumes:
      - .:/app
    ports:
      - "8000:8000"
```

## 🔍 IDE Configuration

### VS Code / Cursor Setup

**Recommended Extensions:**
- Python (Microsoft)
- Pylint
- Black Formatter
- Test Explorer
- GitLens

**.vscode/settings.json:**
```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"],
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black"
}
```

**.vscode/launch.json (Debugging):**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Transcription Job",
      "type": "python",
      "request": "launch",
      "program": "run_transcription_job.py",
      "env": {
        "RUNPOD_ENDPOINT": "https://your-endpoint.com"
      }
    }
  ]
}
```

## 🚨 Troubleshooting

### Common Issues

**1. CommonUtils Import Errors:**
```bash
# Fix: Ensure submodule is initialized
git submodule update --init --recursive
cd common-utils && pip install -e . && cd ..
```

**2. RunPod Connection Errors:**
```bash
# Fix: Verify environment variable
echo $RUNPOD_ENDPOINT
# Should show your endpoint URL

# Test connection
curl -X POST $RUNPOD_ENDPOINT/health
```

**3. Test Failures:**
```bash
# Fix: Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run with verbose output
pytest -v -s tests/
```

**4. Import Path Issues:**
```bash
# Fix: Add to PYTHONPATH
export PYTHONPATH="${PWD}:${PWD}/common-utils:${PYTHONPATH}"

# Or use development installation
pip install -e .
```

### Performance Issues

**Slow RSS Parsing:**
```bash
# Check feed responsiveness
curl -w "%{time_total}" https://example.com/feed.rss

# Profile parsing performance
python -m cProfile rss_parser.py
```

**Memory Usage:**
```bash
# Monitor memory during processing
python -m memory_profiler run_transcription_job.py
```

## 📊 Development Workflow

### Daily Development Cycle

1. **Start Development:**
   ```bash
   cd SpiceflowNavigator-Ingest
   source .venv/bin/activate
   make test  # Verify everything works
   ```

2. **Work on Features:**
   ```bash
   # Create feature branch
   git checkout -b feature/real-time-monitoring
   
   # Make changes, run tests frequently
   make test-unit
   ```

3. **Before Committing:**
   ```bash
   make lint      # Fix code style
   make test      # Full test suite
   make check-deps # Verify no new dependencies
   ```

4. **Commit and Push:**
   ```bash
   git add .
   git commit -m "feat: implement real-time RSS monitoring"
   git push origin feature/real-time-monitoring
   ```

### Integration with Other Agents

**CommonUtils Updates:**
```bash
# Pull latest CommonUtils changes
cd common-utils
git pull origin main
cd ..

# Test compatibility
make test
```

**Cross-Agent Coordination:**
```bash
# Check if your changes affect other agents
make check-common-utils  # Verify CommonUtils compatibility
```

## 🎯 Ready to Develop!

Your Navigator-Ingest development environment is now configured for:
- ✅ **Independent development** with no cross-agent conflicts
- ✅ **Codex-optimized structure** for AI-assisted development
- ✅ **Comprehensive testing** with unit and integration tests
- ✅ **CommonUtils integration** with stability guarantees
- ✅ **Production-ready workflows** with CI/CD support

**Start building the future of content ingestion!** 🚀

---

## 📞 Support

**Issues & Questions:**
- Repository Issues: [GitHub Issues](https://github.com/pa5tabear/SpiceflowNavigator-Ingest/issues)
- Architecture Questions: See `docs/DEV_GUIDE.md` in main repo
- CommonUtils Changes: Follow `common-utils/API_SAFETY.md` protocol

**Happy coding!** 🎯 
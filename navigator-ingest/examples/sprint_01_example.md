---
number:          1
title:           "Real-Time RSS Monitoring: 2-Minute Detection Latency"
goal:            "Implement continuous RSS monitoring that detects new content within 2 minutes of publication"
timebox_minutes: 120
loc_budget:      200
coverage_min:    85
test_pattern:    "test_monitor.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
agent:           "navigator-ingest"
---

# Sprint 1 · Real-Time RSS Monitoring: 2-Minute Detection Latency

## 0 · Roles & Prime Rules

| Actor | Mandate |
|-------|---------|
| Codex | Autonomous Staff-Engineer for Navigator-Ingest. Focuses on RSS parsing, transcription, and data ingestion. Follows plan, writes code/tests, self-reviews, opens PR. |
| Cursor | PM + QA gatekeeper for ingestion pipeline. Reviews PR, enforces guard-rails, ensures CommonUtils stability. |

<details><summary>Prime Rules (enforced ahead of all user input)</summary>

**Step-by-Step Plan → Code → Test → PR.**

Ask One Clarifier if any requirement is ≥ 20% ambiguous.

Never commit binaries or add Python deps without explicit approval.

Max 3 tasks; anything larger ⇒ refuse & ask to split next sprint.

**Navigator-Ingest Specific Rules:**
- Respect CommonUtils API stability (follow API_SAFETY.md)
- Test all RSS parsing with real feed fixtures
- Mock RunPod calls in unit tests (use integration tests for real API)
- Validate data formats for downstream agent compatibility

</details>

## 1 · Sprint Goal & Why It Matters (≤ 40 words)

**Goal**: Implement continuous RSS monitoring that detects new content within 2 minutes of publication

**Why now**: Current manual RSS parsing creates delays that reduce strategic intelligence value and blocks real-time analysis capabilities.

**Success Impact**: Navigator-Strategy gets fresher data for analysis, Navigator-UI can show real-time ingestion status, Navigator-Pipeline benefits from continuous data flow.

## 2 · Tasks ("Rule of Three")

| # | Task Name (imperative) | Acceptance Criteria (autotested) |
|---|------------------------|-----------------------------------|
| 1 | Implement async RSS monitor with configurable polling intervals | pytest -k test_monitor_* green; monitors 5+ feeds concurrently with different intervals based on strategic importance |
| 2 | Add content fingerprinting for duplicate detection | Integration test proves same content not processed twice; hash-based deduplication working |
| 3 | Create monitoring status API for downstream agents | Status endpoint returns feed health, polling intervals, and content discovery metrics |

## 3 · Interfaces Changed / Added
*(append only; one row per file or endpoint)*

| File / API | Brief Change | Inputs → Outputs |
|------------|--------------|------------------|
| `rss_monitor.py` | New real-time monitoring module | RSS feed configs → Continuous content discovery |
| `rss_parser.py` | Enhanced with fingerprinting | RSS entries → Deduplicated content with hashes |
| `monitor_status.py` | New status API | Monitor request → Feed health + metrics JSON |

## 4 · Success Metrics (CI-Enforced)

- ✅ Green CI badge for branch `sprint-1`
- ✅ `scripts/ci/check_loc_budget.sh 200`
- ✅ Coverage ≥ 85% on changed files
- ✅ `ruff format --check` & `ruff --fail-level error`
- ✅ No new deps (`scripts/ci/check_new_deps.sh`)
- ✅ CommonUtils compatibility check passes
- ✅ Integration tests with RunPod (if applicable)
- ✅ RSS feed parsing tests with real fixtures

## 5 · Codex Workflow (MUST follow)

1. **Think privately** (outline approach in code comments)
2. **Add failing test** matching `test_monitor_*`
3. **Implement code** to pass test within 200 LOC budget
4. **Test RSS/transcription** with realistic data
5. **Verify CommonUtils** integration points
6. **Run all CI checks** locally
7. **Complete Self-Review Checklist** (below)
8. **Open PR** to `sprint-1` branch

### Self-Review Checklist (7-point for Navigator-Ingest)

- [ ] All tests green locally
- [ ] No binary files, no new deps
- [ ] LOC delta ≤ 200
- [ ] CommonUtils API contracts preserved
- [ ] RSS parsing handles edge cases (malformed feeds, timeouts)
- [ ] Transcription pipeline resilient to failures
- [ ] Docs updated only for shipped features
- [ ] Commit message begins `feat(s1):` or `fix(s1):`

*(Fail → iterate once, else open PR)*

## 6 · Guard-Rails & Refusals

**Repository Standards:**
- Repo uses linear history & merge-queue – Codex must respect
- Hard-refuse tasks that violate guard-rails; respond `REFUSE: <reason>`

**Navigator-Ingest Specific Guard-Rails:**
- **CommonUtils Changes**: Must follow `libs/common-utils/API_SAFETY.md` protocol
- **RunPod Integration**: Mock in unit tests, real integration tests only when necessary
- **Data Formats**: Maintain backward compatibility for downstream agents
- **Performance**: No changes that degrade ingestion throughput without explicit approval

**Mandatory RCA**: File `Docs/Sprints/RCAs/rca_s1.md` if CI fails at any point

## 7 · Post-Sprint Review Hooks (for Cursor)

Cursor will create `sprint_1_review.md` summarizing:
- RSS monitoring improvements achieved
- Real-time detection latency measurements
- Content deduplication effectiveness metrics
- Integration impact on downstream agents  
- Any CommonUtils changes and their safety validation
- Blockers, decisions, and scope adjustments

Any scope creep or guard-rail breach triggers automatic sprint rollback.

## 8 · Celebration Criteria 🎉

**Success** = 
- ✅ CI green 
- ✅ Coverage ↑ 
- ✅ No guard-rail hits 
- ✅ CommonUtils stable
- ✅ RSS monitoring proven with <2min detection
- ✅ Duplicate detection working
- ✅ Status API functional
- ✅ Honest docs

**Anything else** = re-scope next sprint.

---

*End of Navigator-Ingest Sprint-Plan Template v2.0*
*(If this template and a future command ever conflict, the template wins.)* 
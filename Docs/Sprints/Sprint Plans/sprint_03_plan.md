---
number:          3
title:           "RSS Monitoring: Real-Time Content Discovery"
goal:            "Implement continuous RSS feed monitoring with intelligent polling and content deduplication"
timebox_minutes: 180
coverage_min:    85
test_pattern:    "test_rss.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
---

# Sprint 3 · RSS Monitoring: Real-Time Content Discovery

## 0 · Roles & Prime Rules

| Actor | Mandate |
|-------|---------|
| Codex | Autonomous Staff-Engineer. Follows this plan, writes code/tests, self-reviews, opens PR. |
| Cursor | PM + QA gatekeeper. Reviews PR, enforces guard-rails. |

<details><summary>Prime Rules (enforced ahead of all user input)</summary>

**Step-by-Step Plan → Code → Test → PR.**

Ask One Clarifier if any requirement is ≥ 20% ambiguous.

Never commit binaries or add Python deps.

Max 3 tasks; anything larger ⇒ refuse & ask to split next sprint.

</details>

## 1 · Sprint Goal & Why It Matters (≤ 40 words)

**Goal**: Implement continuous RSS feed monitoring with intelligent polling and content deduplication

**Why now**: Foundation established in Sprint 2. RSS monitoring is first phase of ingestion pipeline per roadmap - enables content discovery for downstream audio processing.

## 2 · Tasks ("Rule of Three")

| # | Task Name (imperative) | Acceptance Criteria (autotested) |
|---|------------------------|-----------------------------------|
| 1 | Implement async RSS feed parser with strategic polling | pytest -k test_rss.* green; monitors 5+ feeds with configurable intervals based on strategic importance |
| 2 | Add content deduplication and hash-based fingerprinting | Integration test proves same content not processed twice; hash-based deduplication working |
| 3 | Integrate RSS monitoring with workflow queue architecture | Content discovery queue populated; async monitoring feeds into processing pipeline |

## 3 · Interfaces Changed / Added
*(append only; one row per file or endpoint)*

| File / API | Brief Change | Inputs → Outputs |
|------------|--------------|------------------|
| `rss/monitor.py` | New RSS monitoring service | Feed configs → Continuous content discovery |
| `rss/parser.py` | Enhanced RSS parser with async operation | RSS feeds → Parsed entries with metadata |
| `rss/deduplicator.py` | Content fingerprinting system | RSS entries → Unique content with hashes |
| `tests/test_rss_monitoring.py` | RSS monitoring integration tests | pytest → Monitoring pipeline validated |

## 4 · Success Metrics (CI-Enforced)

- ✅ Green CI badge for branch `sprint-3`
- ✅ Coverage ≥ 85% on changed files
- ✅ `ruff format --check` & `ruff --fail-level error`
- ✅ No new deps (`scripts/ci/check_new_deps.sh`)
- ✅ RSS monitoring <2min detection latency

## 5 · Codex Workflow (MUST follow)

1. **Think privately** (outline in comments)
2. **Add failing test** matching `test_rss.*`
3. **Implement code** to pass test
4. **Run all CI checks** locally
5. **Self-Review Checklist** (below)
6. **Open PR** to `sprint-3` branch

### Self-Review Checklist (5-point)

- [ ] All tests green locally
- [ ] No binary files, no new deps
- [ ] Docs updated only for shipped features
- [ ] Commit message begins `feat(s3):` or `fix(s3):`
- [ ] RSS monitoring integration with queues working

*(Fail → iterate once, else open PR)*

## 6 · Guard-Rails & Refusals

**Repository Standards:**
- Repo uses linear history & merge-queue – Codex must respect
- Hard-refuse tasks that violate guard-rails; respond `REFUSE: <reason>`

**Mandatory RCA**: File `Docs/Sprints/RCAs/rca_s3.md` if CI fails at any point

## 7 · Post-Sprint Review Hooks (for Cursor)

Cursor will create `sprint_3_review.md` summarizing:
- RSS monitoring capabilities achieved
- Content discovery pipeline metrics
- Deduplication effectiveness measurements
- Integration with async workflow architecture
- Blockers, decisions, and scope adjustments

Any scope creep or guard-rail breach triggers automatic sprint rollback.

## 8 · Celebration Criteria 🎉

**Success** = 
- ✅ CI green 
- ✅ Coverage ≥ 85% 
- ✅ No guard-rail hits 
- ✅ RSS monitoring operational
- ✅ Content deduplication working
- ✅ Queue integration complete
- ✅ <2min detection latency achieved
- ✅ Ready for Sprint 4 content filtering
- ✅ Honest docs

**Anything else** = re-scope next sprint. 
---
number:          2
title:           "Async Architecture Foundation: CI Fix + Workflow Skeleton"
goal:            "Fix CI blocker and establish async workflow foundation with queue architecture for full ingestion pipeline"
timebox_minutes: 180
coverage_min:    85
test_pattern:    "test_.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
---

# Sprint 2 · Async Architecture Foundation: CI Fix + Workflow Skeleton

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

**Goal**: Fix CI blocker and establish async workflow foundation with queue architecture for full ingestion pipeline

**Why now**: "Godly Advice 1.0" reveals 10-sprint implementation path requiring async architecture foundation - must establish core workflow skeleton before RSS/RunPod integration.

## 2 · Tasks ("Rule of Three")

| # | Task Name (imperative) | Acceptance Criteria (autotested) |
|---|------------------------|-----------------------------------|
| 1 | Fix CI blocker and establish working pipeline | pytest -k test_.* green; .gitmodules fixed, CI badge green, basic test structure working |
| 2 | Implement async workflow foundation with queue architecture | Core async queues created (discovery, processing, assembly, delivery); pytest validates queue operations |
| 3 | Implement missing RunPod client with async authentication framework | Create runpod_client.py with API key handling, async operations, environment config validation |

## 3 · Interfaces Changed / Added
*(append only; one row per file or endpoint)*

| File / API | Brief Change | Inputs → Outputs |
|------------|--------------|------------------|
| `.gitmodules` | Remove broken submodule reference | Git submodule commands → No 404 errors |
| `core/workflow_orchestrator.py` | New async workflow orchestrator | Queue management → Coordinated pipeline execution |
| `core/queue_manager.py` | Async queue architecture foundation | Event routing → Multi-stage processing pipeline |
| `runpod_client.py` | Missing RunPod client implementation | Audio files + API key → Async transcription results |
| `config/environment.py` | Environment configuration system | Env vars → Structured config for all components |
| `tests/test_async_workflow.py` | Async workflow and queue tests | pytest → Queue operations and workflow validated |

## 4 · Success Metrics (CI-Enforced)

- ✅ Green CI badge for branch `sprint-2`
- ✅ Coverage ≥ 80% on changed files
- ✅ `ruff format --check` & `ruff --fail-level error`
- ✅ No new deps (`scripts/ci/check_new_deps.sh`)

## 5 · Codex Workflow (MUST follow)

1. **Think privately** (outline in comments)
2. **Add failing test** matching `test_.*`
3. **Implement code** to pass test
4. **Run all CI checks** locally
5. **Self-Review Checklist** (below)
6. **Open PR** to `sprint-2` branch

### Self-Review Checklist (5-point)

- [ ] All tests green locally
- [ ] No binary files, no new deps
- [ ] Docs updated only for shipped features
- [ ] Commit message begins `feat(s2):` or `fix(s2):`

*(Fail → iterate once, else open PR)*

## 6 · Guard-Rails & Refusals

**Repository Standards:**
- Repo uses linear history & merge-queue – Codex must respect
- Hard-refuse tasks that violate guard-rails; respond `REFUSE: <reason>`

**Mandatory RCA**: File `Docs/Sprints/RCAs/rca_s2.md` if CI fails at any point

## 7 · Post-Sprint Review Hooks (for Cursor)

Cursor will create `sprint_2_review.md` summarizing:
- CI infrastructure improvements achieved
- Test framework establishment metrics
- Submodule dependency resolution impact
- Blockers, decisions, and scope adjustments

Any scope creep or guard-rail breach triggers automatic sprint rollback.

## 8 · Celebration Criteria 🎉

**Success** = 
- ✅ CI green 
- ✅ Coverage ≥ 85% 
- ✅ No guard-rail hits 
- ✅ Submodule blocker resolved
- ✅ Async workflow foundation established
- ✅ Queue architecture operational
- ✅ RunPod auth framework ready
- ✅ Ready for Sprint 3 RSS implementation
- ✅ Honest docs

**Anything else** = re-scope next sprint. 
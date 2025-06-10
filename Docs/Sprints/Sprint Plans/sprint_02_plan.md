---
number:          2
title:           "CI Infrastructure Fix: Enable Development Workflow"
goal:            "Resolve submodule blocker and establish working CI pipeline with basic test validation"
timebox_minutes: 90
coverage_min:    80
test_pattern:    "test_.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
---

# Sprint 2 · CI Infrastructure Fix: Enable Development Workflow

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

**Goal**: Resolve submodule blocker and establish working CI pipeline with basic test validation

**Why now**: Critical CI blocker prevents all code validation, testing, and development workflow - must fix before any feature development can proceed.

## 2 · Tasks ("Rule of Three")

| # | Task Name (imperative) | Acceptance Criteria (autotested) |
|---|------------------------|-----------------------------------|
| 1 | Remove broken common-utils submodule dependency | pytest -k test_.* green; .gitmodules cleaned, no 404 errors in CI checkout |
| 2 | Create basic test structure with smoke tests | CI runs test discovery successfully; tests/ directory with working import validation |
| 3 | Verify end-to-end CI pipeline functionality | CI badge shows green; all workflow steps complete without infrastructure failures |

## 3 · Interfaces Changed / Added
*(append only; one row per file or endpoint)*

| File / API | Brief Change | Inputs → Outputs |
|------------|--------------|------------------|
| `.gitmodules` | Remove broken submodule reference | Git submodule commands → No 404 errors |
| `tests/__init__.py` | New test package structure | Test discovery → Basic test suite found |
| `tests/test_smoke.py` | Basic import validation tests | pytest → Core modules importable |

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
- ✅ Coverage ↑ 
- ✅ No guard-rail hits 
- ✅ Submodule blocker resolved
- ✅ Basic test structure working
- ✅ Development workflow unblocked
- ✅ Honest docs

**Anything else** = re-scope next sprint. 
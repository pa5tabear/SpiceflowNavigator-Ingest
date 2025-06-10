---
number:          7
title:           "Fix Test Infrastructure & Environment"
goal:            "Resolve failing tests and stabilize CI for subsequent feature development"
timebox_minutes: 120
coverage_min:    95
test_pattern:    "test_.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
---

# Sprint 7 · Fix Test Infrastructure & Environment

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

## 1 · Sprint Goal & Why It Matters (≤ 25 words)

**Goal**: Resolve failing tests and stabilize CI for subsequent feature development

**Why now**: Pattern of sprint non-execution and persistent test failure blocking development progress. Foundation must be stable before audio processing.

## 2 · Deliverables & Acceptance Criteria

• **Fix RunPod client test configuration**  
  Resolve `test_async_transcribe` environment variable failure by proper test environment setup

• **Consolidate environment configuration**  
  Ensure consistent environment loading pattern across all modules without breaking existing functionality

• **Add simple audio placeholder implementation**  
  Minimal audio downloader stub to unblock future sprints without full concurrent implementation

## 4 · Workflow

1. **Think** → Analyze test failure root cause and environment configuration patterns
2. **Plan** → Design minimal fixes for test stability without breaking existing functionality  
3. **Code** → Implement targeted fixes for failing tests and basic audio placeholder
4. **Test** → Verify 100% test pass rate and no regressions

## 5 · Self-Review Rubric

- [ ] All tests green locally including fixed RunPod test
- [ ] No binary files, no new deps beyond existing requirements
- [ ] Environment configuration consistent across modules
- [ ] Audio placeholder enables future development
- [ ] Commit message begins `fix(s7):` or `refactor(s7):`

## 6 · Proposed Next Sprint

Sprint 8: Audio processing pipeline implementation with full download and validation system. 
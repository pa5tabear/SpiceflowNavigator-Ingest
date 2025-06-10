---
number:          5
title:           "Consolidated Recovery: RSS Foundation + Test Fixes"
goal:            "Complete all missing RSS monitoring deliverables and resolve persistent test failures"
timebox_minutes: 240
coverage_min:    85
test_pattern:    "test_.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
---

# Sprint 5 · Consolidated Recovery: RSS Foundation + Test Fixes

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

**Goal**: Complete all missing RSS monitoring deliverables and resolve persistent test failures

**Why now**: Sprints 3+4 non-delivery risks entire roadmap. Consolidated recovery essential before audio processing phase.

## 2 · Deliverables & Acceptance Criteria

• **Fix environment configuration and test failures**  
  All 11 tests pass including async transcribe; environment properly mocked without external dependencies

• **Implement complete RSS monitoring pipeline**  
  RSS monitor service with async polling, content detection, hash-based deduplication operational

• **Integrate RSS content with workflow queues**  
  RSS content flows into discovery queue; queue integration tested and functional end-to-end

## 4 · Workflow

1. **Think** → Analyze Sprint 3+4 gaps, prioritize critical path components
2. **Plan** → Design minimal viable RSS pipeline with proper test coverage
3. **Code** → Implement RSS monitoring with queue integration, fix environment issues
4. **Test** → Validate all functionality, ensure 100% test pass rate

## 5 · Self-Review Rubric

- [ ] All tests green locally (11/11 passing, zero failures)
- [ ] No binary files, no new deps
- [ ] RSS monitoring fully implemented per original Sprint 3 plan
- [ ] Environment configuration working without external setup
- [ ] Commit message begins `feat(s5):` or `fix(s5):`

## 6 · Proposed Next Sprint

Sprint 6: Audio processing pipeline implementation per roadmap Phase 2. 
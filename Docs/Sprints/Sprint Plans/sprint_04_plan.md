---
number:          4
title:           "RSS Monitoring Completion: Content Discovery Pipeline"
goal:            "Complete missing RSS monitoring components and fix test failures from Sprint 3"
timebox_minutes: 120
coverage_min:    85
test_pattern:    "test_rss.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
---

# Sprint 4 · RSS Monitoring Completion: Content Discovery Pipeline

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

**Goal**: Complete missing RSS monitoring components and fix test failures from Sprint 3

**Why now**: Sprint 3 deliverables incomplete - RSS foundation required before Sprint 5 audio processing can proceed per roadmap.

## 2 · Deliverables & Acceptance Criteria

• **Fix test failures and environment configuration**  
  All tests pass including async transcribe; environment setup properly mocked in tests

• **Implement RSS monitoring service with async polling**  
  RSS monitor class created with configurable feed polling and content detection working

• **Add content deduplication and queue integration**  
  Hash-based deduplication operational; RSS content flows into workflow queues successfully

## 4 · Workflow

1. **Think** → Review Sprint 3 gaps, identify missing components
2. **Plan** → Design RSS monitor service and deduplication approach  
3. **Code** → Implement missing components with proper async patterns
4. **Test** → Ensure all RSS monitoring tests pass with queue integration

## 5 · Self-Review Rubric

- [ ] All tests green locally (11/11 passing)
- [ ] No binary files, no new deps beyond Sprint 3 additions
- [ ] RSS monitoring components fully implemented per Sprint 3 plan
- [ ] Queue integration working with content discovery
- [ ] Commit message begins `feat(s4):` or `fix(s4):`

## 6 · Proposed Next Sprint

Sprint 5: Audio processing pipeline implementation with download and validation per roadmap. 
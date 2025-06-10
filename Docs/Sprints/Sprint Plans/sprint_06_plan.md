---
number:          6
title:           "Audio Processing Pipeline: Download & Validation"
goal:            "Implement concurrent audio download and validation system with file management"
timebox_minutes: 180
coverage_min:    85
test_pattern:    "test_audio.*"
template_version: 2.0 (2025-06-08)
require_golden_path: false
---

# Sprint 6 · Audio Processing Pipeline: Download & Validation

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

**Goal**: Implement concurrent audio download and validation system with file management

**Why now**: RSS foundation complete from Sprint 5. Audio processing is roadmap Phase 2 - enables content preparation for RunPod transcription.

## 2 · Deliverables & Acceptance Criteria

• **Implement async audio download with concurrency control**  
  Audio downloader class with semaphore-based concurrency limits, handles large files with streaming download

• **Add audio file validation using ffprobe integration**  
  Audio validator extracts metadata (duration, format, bitrate), validates file integrity, handles corrupted files

• **Create temporary file management and cleanup system**  
  File manager handles temp directory creation, automatic cleanup, tracks downloaded files for processing pipeline

## 4 · Workflow

1. **Think** → Review RSS→audio flow, design download and validation pipeline
2. **Plan** → Design concurrent download strategy with validation integration
3. **Code** → Implement audio processor components with proper async patterns
4. **Test** → Validate download, file validation, and cleanup functionality

## 5 · Self-Review Rubric

- [ ] All tests green locally including new audio tests
- [ ] No binary files, no new deps beyond existing requirements
- [ ] Audio download and validation working with queue integration
- [ ] Temporary file management robust with cleanup
- [ ] Commit message begins `feat(s6):` or `fix(s6):`

## 6 · Proposed Next Sprint

Sprint 7: Audio chunking implementation for optimal RunPod transcription per roadmap. 
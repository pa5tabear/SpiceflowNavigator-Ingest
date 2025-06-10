# Sprint 9 Plan
**Date:** 2025-06-10  
**PM/QA:** Cursor v3.0  
**Priority:** P0 - Infrastructure Fix

## 1 · Sprint Goal (≤25 words)
Resolve critical CI blocker by fixing broken submodule dependency and establish working test pipeline for development validation.

## 2 · Deliverables & Acceptance Criteria

### Task 1: Fix Submodule Dependency
- **AC1:** Remove or replace broken `common-utils` submodule reference in `.gitmodules`
- **AC2:** Update any imports/dependencies that relied on common-utils
- **AC3:** CI checkout step passes without submodule errors

### Task 2: Establish Working CI Pipeline  
- **AC1:** All CI jobs run to completion (no infrastructure failures)
- **AC2:** Basic Python linting/syntax validation passes
- **AC3:** Test discovery runs successfully (even if 0 tests found)

### Task 3: Create Basic Test Structure
- **AC1:** Add `tests/` directory with `__init__.py`
- **AC2:** Create one smoke test that validates core module imports
- **AC3:** CI runs test suite and reports results (pass/fail/count)

## 4 · Workflow
1. **Think:** Analyze `.gitmodules` and identify all common-utils dependencies
2. **Plan:** Decide on removal vs. replacement strategy for submodule
3. **Code:** Update `.gitmodules`, fix imports, create basic test structure  
4. **Test:** Verify CI runs green end-to-end with new configuration

## 5 · Self-Review Rubric
- [ ] `.gitmodules` file updated (removed broken reference)
- [ ] No remaining imports from `common-utils` without replacement
- [ ] CI workflow file (`.github/workflows/ci.yml`) unchanged unless necessary
- [ ] Basic test file exists and imports core modules successfully
- [ ] All changes committed with clear messages
- [ ] CI passes on feature branch before PR

## 6 · Proposed Next Sprint
Sprint 10: RSS ingestion pipeline implementation with working CI validation. 
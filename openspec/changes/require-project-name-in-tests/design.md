## Context

Integration tests in `test_github_integration.py` currently support two modes for project naming:
1. Use `TRACKER_GITHUB_PROJECT_NAME` if set in `.env.test`
2. Fall back to auto-generated name: `Migration Agent Test - {org} - {timestamp}`

The auto-generation fallback was originally added for convenience, allowing developers to run tests without explicit project name configuration. However, this creates ambiguity about which projects are intentional test fixtures vs. accidentally created resources.

Current code path in `test_create_project()`:
```python
project_name = config.get('project_name') or generate_test_project_name(config['organization'])
```

The Makefile `env-check` target validates `TRACKER_GITHUB_TOKEN` and `TRACKER_GITHUB_ORGANIZATION` but does not validate `TRACKER_GITHUB_PROJECT_NAME`.

## Goals / Non-Goals

**Goals:**
- Make `TRACKER_GITHUB_PROJECT_NAME` a required field for integration tests
- Fail fast with clear error message if project name not configured
- Validate project name before any GitHub API calls
- Remove auto-generation fallback to enforce explicit naming
- Update all documentation to reflect required field
- Maintain backward compatibility with existing `.env.test` files that have project name set

**Non-Goals:**
- Change production code behavior (this is test infrastructure only)
- Validate project name format or GitHub naming conventions
- Auto-create `.env.test` file or prompt for project name interactively
- Change how tests create or delete GitHub Projects (just naming source)

## Decisions

### Decision 1: Validation location - Python script vs. Makefile

**Options:**
- A) Validate in Makefile `env-check` target only
- B) Validate in Python test script only
- C) Validate in both Makefile and Python script

**Choice: C - Validate in both**

**Rationale:**
- Makefile validation provides fast feedback before running Python
- Python validation catches cases where tests run directly without `make`
- Dual validation ensures robustness regardless of invocation method
- Minimal overhead - validation is cheap

**Implementation:**
- Makefile: Add check for `TRACKER_GITHUB_PROJECT_NAME` in `env-check` target
- Python: Add `validate_test_config()` function called in `load_test_config()`

### Decision 2: Error message format

**Options:**
- A) Simple error: "TRACKER_GITHUB_PROJECT_NAME is required"
- B) Detailed error with context and examples
- C) Interactive prompt to set value

**Choice: B - Detailed error with context**

**Rationale:**
- New developers need context about why field is required
- Examples help developers understand expected format
- Non-interactive approach maintains CI/CD compatibility
- Error should point to documentation for full setup guide

**Error message template:**
```
IntegrationTestError: TRACKER_GITHUB_PROJECT_NAME is required in .env.test

Integration tests require an explicit project name to be set.

To fix:
1. Edit .env.test
2. Set: TRACKER_GITHUB_PROJECT_NAME=My Test Project Name
3. Re-run tests

Example:
  TRACKER_GITHUB_PROJECT_NAME=Integration Test Environment

See SETUP_TESTING.md for complete setup guide.
```

### Decision 3: Handle empty string vs. missing variable

**Options:**
- A) Treat empty string as valid (allows intentionally empty names)
- B) Reject empty string same as missing variable
- C) Warn on empty but allow

**Choice: B - Reject empty string**

**Rationale:**
- Empty project names are invalid in GitHub
- No legitimate use case for empty string
- Failing fast prevents confusing GitHub API errors later
- Consistent with treating missing and empty as "not configured"

**Implementation:**
```python
if not config.get('project_name'):
    raise IntegrationTestError("TRACKER_GITHUB_PROJECT_NAME is required...")
```

### Decision 4: Deprecation of `generate_test_project_name()` function

**Options:**
- A) Remove function entirely
- B) Keep function but don't call it
- C) Mark function as deprecated with warning

**Choice: B - Keep function but don't call it**

**Rationale:**
- Function might be useful for other test utilities in future
- Removing it is not necessary to achieve goal
- No runtime cost to keeping unreferenced function
- Can be removed later if truly unused

**Implementation:**
- Remove call to `generate_test_project_name()` in `test_create_project()`
- Keep function definition for potential future use
- Add docstring note that it's no longer used by default tests

### Decision 5: Update .env.test.example format

**Options:**
- A) Leave commented out with note "(required)"
- B) Uncomment with placeholder value
- C) Uncomment with example value

**Choice: C - Uncomment with example value**

**Rationale:**
- Developers copy .env.test.example to .env.test, so uncommented lines are clearer
- Example value shows expected format
- Makes it obvious this is required, not optional
- Developers naturally replace example with their own value

**New format in .env.test.example:**
```bash
# Required: Project name for integration tests
TRACKER_GITHUB_PROJECT_NAME=My Integration Test Project
```

## Risks / Trade-offs

### Risk: Breaking change for existing developers
**Mitigation:**
- Most developers likely already have `TRACKER_GITHUB_PROJECT_NAME` set from previous runs
- Clear error message guides developers to fix
- Documentation update in SETUP_TESTING.md provides easy fix
- This is test infrastructure, not production, so blast radius is limited

### Risk: CI/CD pipelines may not have project name set
**Mitigation:**
- Audit CI/CD configurations before merging
- Update any CI workflows to include `TRACKER_GITHUB_PROJECT_NAME`
- Consider using repo name or branch name as default in CI if needed

### Trade-off: Less convenience vs. more clarity
**Acceptance:**
- Explicit configuration is better than implicit behavior
- One-time setup cost is minimal
- Long-term benefit: clearer test environments and reduced orphaned projects

### Risk: Developers might use same project name across different test runs
**Acceptance:**
- This is actually desirable for local development (consistent test project)
- Tests still create/delete project each run
- No conflict if same name used multiple times sequentially

## Migration Plan

**For existing developers:**
1. Pull latest changes
2. Run `make test-integration`
3. If error about missing project name:
   - Edit `.env.test`
   - Add `TRACKER_GITHUB_PROJECT_NAME=My Test Project`
   - Re-run tests
4. No code changes needed

**For new developers:**
- Follow updated `SETUP_TESTING.md` which includes project name in required steps
- `make env-setup` creates `.env.test` from updated template with example value

**Rollback:**
- If blocking adoption, can temporarily add back auto-generation with warning
- Recommended: Push forward with clear documentation instead

## Open Questions

None - design is straightforward with clear implementation path.

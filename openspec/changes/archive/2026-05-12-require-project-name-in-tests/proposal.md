## Why

Integration tests currently allow auto-generated project names with timestamps, which creates several issues: (1) Developers don't explicitly choose test project names, leading to confusion about which projects are test artifacts, (2) Auto-generated names make it harder to recognize and manage test projects in GitHub UI, (3) Tests can create orphaned projects if cleanup fails, with no clear ownership. Requiring explicit project names improves test clarity, makes test projects easily identifiable, and encourages developers to think about test environment setup.

## What Changes

- Require `TRACKER_GITHUB_PROJECT_NAME` to be set in `.env.test` for integration tests
- Remove auto-generation fallback in `test_github_integration.py` - fail fast if not configured
- Add validation in test setup that fails with clear error message if project name not set
- Update `.env.test.example` to make `TRACKER_GITHUB_PROJECT_NAME` required (not optional)
- Update all testing documentation to reflect that custom project name is mandatory
- Add `make env-check` validation to verify project name is configured before running tests
- Keep project creation capability - tests still create GitHub Projects, just with user-specified names

## Capabilities

### New Capabilities
- `test-config-validation`: Validation of required test configuration fields before test execution

### Modified Capabilities
<!-- No existing spec-level requirement changes - this is test infrastructure only -->

## Impact

**Files Modified:**
- `agents/project-tracker-agent/tests/integration/test_github_integration.py` - Add validation, remove auto-generation
- `agents/project-tracker-agent/.env.test.example` - Make TRACKER_GITHUB_PROJECT_NAME required
- `agents/project-tracker-agent/Makefile` - Update env-check to validate project name
- `agents/project-tracker-agent/TESTING.md` - Document required field
- `agents/project-tracker-agent/README.md` - Update integration test section
- `agents/project-tracker-agent/SETUP_TESTING.md` - Update setup instructions
- `agents/project-tracker-agent/TEST_QUICK_REFERENCE.md` - Update requirements table

**User Impact:**
- **BREAKING**: Developers must now set `TRACKER_GITHUB_PROJECT_NAME` in `.env.test` before running integration tests
- Tests fail fast with clear error message if project name not configured
- No impact on production code - only affects integration test setup

**Benefits:**
- Explicit test project naming improves clarity
- Easier to identify test projects in GitHub UI
- Better test environment control and ownership
- Reduced risk of orphaned test projects
- Encourages thoughtful test environment setup

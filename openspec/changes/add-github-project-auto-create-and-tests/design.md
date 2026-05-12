## Context

Currently, GitHubProjectsTracker requires users to:
1. Manually create a GitHub Project in their organization/repo
2. Note the project number from the URL
3. Configure TRACKER_GITHUB_PROJECT_NUMBER

This creates friction for new users who just want to try GitHub integration. Additionally, there's no way to validate the GitHub tracker works without manual testing against a real GitHub instance.

Current state:
- GitHubProjectsTracker only reads from existing projects
- No automated way to validate GitHub API integration
- Manual testing is error-prone and time-consuming
- Users must understand GitHub Projects v2 before trying the tracker

Constraints:
- Must not break existing workflows (explicit project_number continues to work)
- GitHub API has rate limits (5000/hour authenticated)
- Created projects should be clearly marked as auto-generated
- Test projects must be cleaned up to avoid clutter

## Goals / Non-Goals

**Goals:**
- Auto-create GitHub Project when project_number is omitted
- Provide integration test script that validates end-to-end GitHub tracker functionality
- Use .env.test for test configuration (separate from production .env)
- Test script creates project, adds items, updates status, verifies, and cleans up
- Make GitHub integration testing reproducible and automated
- Provide clear output showing what was created and whether tests passed

**Non-Goals:**
- Auto-create projects for every migration (only when project_number missing)
- Support for GitHub Projects v1 (classic projects)
- Automated cleanup of production projects (only test projects)
- Migration of existing issues to new projects
- Support for project templates or custom fields in auto-creation

## Decisions

### D1: Auto-Create Only When project_number Omitted

**Decision:** Only auto-create project when TRACKER_GITHUB_PROJECT_NUMBER is not set in configuration

**Rationale:**
- Preserves backward compatibility
- Explicit is better than implicit - if user specifies project number, use it
- Avoids accidentally creating duplicate projects
- Clear opt-in behavior

**Alternatives considered:**
- Always create new project → Rejected: wasteful, breaks existing setups
- Require --create-project flag → Rejected: adds friction, defeats purpose
- Check if project exists, create if not → Rejected: adds complexity, slow startup

### D2: Store Project Number in .env After Creation

**Decision:** After auto-creating project, print project number to console but don't automatically write to .env

**Rationale:**
- User may want to review project before committing to it
- Automated file writes can be surprising
- Easy to add manually or use suggested command
- Keeps tool behavior predictable

**Alternatives considered:**
- Auto-write to .env → Rejected: file mutations can surprise users
- Store in separate .project file → Rejected: adds complexity
- In-memory only → Accepted: simple, user adds to .env if they want to keep it

### D3: Integration Test Uses .env.test

**Decision:** Test script loads configuration from .env.test file, separate from production .env

**Rationale:**
- Prevents accidentally running tests against production project
- Clear separation of test vs production config
- Can commit .env.test.example as documentation
- Follows common testing patterns (.env.test, .env.development, etc.)

**Alternatives considered:**
- Use same .env with TEST_MODE flag → Rejected: risky, could affect production
- Command-line args only → Rejected: verbose, hard to reproduce
- Hardcoded test config → Rejected: not flexible for different setups

### D4: Test Script Structure

**Decision:** Integration test script runs these steps:
1. Load .env.test configuration
2. Create a test project (name: "Migration Test - {timestamp}")
3. Create 3 test issues/items
4. Update status of items (Backlog → In Progress → Done)
5. Verify all operations succeeded
6. Cleanup: Delete test project
7. Report results (pass/fail with details)

**Rationale:**
- Covers complete workflow (create, update, read, delete)
- Timestamp prevents name conflicts
- Cleanup ensures no clutter
- Clear pass/fail output for CI/CD integration

**Alternatives considered:**
- Keep test projects for inspection → Rejected: clutters GitHub
- Test only create/read → Rejected: incomplete validation
- Use existing project → Rejected: doesn't test creation path

### D5: Project Creation GraphQL Mutation

**Decision:** Use createProjectV2 mutation with minimal required fields (ownerId, title)

**Rationale:**
- Simplest API call, fewest moving parts
- Can enhance later with description, fields, etc.
- OwnerId can be organization or user ID
- Title includes "Migration Agent" for clarity

**Alternatives considered:**
- Clone from template → Rejected: requires finding template, more complex
- REST API → Rejected: Projects v2 only available in GraphQL
- Include custom fields on creation → Rejected: overkill for initial version

### D6: Error Handling for Auto-Creation

**Decision:** If project creation fails, log error and fall back to LocalTracker

**Rationale:**
- Migration shouldn't fail just because GitHub is unreachable
- Same pattern as existing GitHub tracker errors
- User can fix config and retry

**Alternatives considered:**
- Fail hard → Rejected: breaks migrations unnecessarily
- Retry with backoff → Considered: good for rate limits but adds complexity
- Prompt user to create manually → Rejected: breaks automated workflows

## Risks / Trade-offs

**[Risk]** Auto-created projects may not have desired configuration (fields, views, automation)
→ **Mitigation:** Document that auto-created projects are basic; users can configure manually or specify existing project

**[Risk]** Test script could fail mid-way leaving orphaned test projects
→ **Mitigation:** Use try/finally to ensure cleanup runs; timestamp in name makes orphans easy to identify and remove manually

**[Risk]** GitHub API rate limits during testing
→ **Mitigation:** Test script checks rate limit before starting; waits if needed; documents rate limit requirements (needs ~10 API calls)

**[Trade-off]** Auto-creation uses additional GitHub API quota
→ **Accepted:** One-time cost, user benefit outweighs quota usage

**[Risk]** Organization permissions may not allow project creation
→ **Mitigation:** Clear error message with link to GitHub permissions documentation

**[Risk]** Test credentials in .env.test could be committed accidentally
→ **Mitigation:** Add .env.test to .gitignore; provide .env.test.example instead; document in README

## Migration Plan

**Phase 1: Add Project Creation to GitHubProjectsTracker**
1. Add _create_project_v2() method
2. Add _get_owner_id() method (resolve organization to node ID)
3. Update __init__ to check if project_number missing
4. If missing and auto_create enabled (default), create project
5. Return project number for user to save

**Phase 2: Create Integration Test Script**
1. Create tests/integration/test_github_integration.py
2. Implement project creation test
3. Implement issue creation and updates
4. Implement cleanup
5. Add detailed logging and assertions

**Phase 3: Documentation and Configuration**
1. Create .env.test.example
2. Update .gitignore for .env.test
3. Document in README how to run integration tests
4. Add troubleshooting for common issues

**Rollback Strategy:**
- Auto-creation is additive, doesn't break existing behavior
- If issues found, user can specify explicit project_number to bypass
- Test script is standalone, can be skipped without affecting functionality
- No database changes or migrations needed

**Deployment:**
- No infrastructure changes
- Works with existing GitHub Projects v2
- User can start using immediately after installing update

## Open Questions

1. Should auto-created projects be marked as "Draft" or some indicator they're auto-generated?
   - Leaning **no** - just use descriptive name like "Migration Agent - {org/repo}"

2. Should integration test run on every PR in CI/CD?
   - Leaning **no** - requires GitHub token, better as manual validation or nightly job
   - Document how to run locally

3. Should we support auto-creating projects at user level vs organization level?
   - Leaning **yes** - detect from TRACKER_GITHUB_ORGANIZATION whether it's org or user
   - Use user(login:) query if not found in organization()

4. What if user wants specific project configuration (custom fields, views)?
   - **Out of scope for v1** - auto-creation is for quick start, advanced users use existing project_number

## Why

Users must manually create GitHub Projects before using the GitHub tracker, creating friction and setup complexity. Auto-creating projects when no project number is specified streamlines onboarding, and an integration test script is needed to validate the GitHub tracker works end-to-end with real API calls.

## What Changes

- Auto-create GitHub Project in repository when TRACKER_GITHUB_PROJECT_NUMBER is not specified
- Store created project number in .env or return it for future use
- Create comprehensive integration test script (tests/integration/test_github_integration.py)
- Test script uses .env.test configuration to create project, add tasks, update status, and cleanup
- Add project creation GraphQL mutations to GitHubProjectsTracker
- Update initialization logic to detect missing project and create it
- Add --create-project flag to explicitly trigger project creation
- Provide cleanup utilities to delete test projects after validation

## Capabilities

### New Capabilities

- `github-project-creation`: Auto-create GitHub Projects v2 via GraphQL API when project_number not specified
- `github-integration-testing`: Comprehensive test script that validates end-to-end GitHub tracker integration with real API
- `test-environment-config`: Support for .env.test configuration file for integration testing

### Modified Capabilities

- `github-projects-tracker`: Extend to support creating projects, not just using existing ones
- `tracker-configuration`: Add optional auto-create flag and project creation parameters

## Impact

- `trackers/github_tracker.py` - Add project creation methods and auto-create logic
- `trackers/config.py` - Add configuration for project auto-creation (name, description)
- `tests/integration/` - New directory for integration tests
- `tests/integration/test_github_integration.py` - Comprehensive GitHub API test script
- `.env.test.example` - Example test configuration file
- `.gitignore` - Add .env.test to prevent committing test credentials
- Documentation - Add setup guide for GitHub auto-creation and testing
- **BREAKING**: None - auto-creation only happens when project_number is omitted

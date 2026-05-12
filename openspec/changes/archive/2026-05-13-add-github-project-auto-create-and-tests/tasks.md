## 1. Add Project Creation to GitHubProjectsTracker

- [x] 1.1 Add _get_owner_id(organization: str) -> str method to resolve org/user to node ID
- [x] 1.2 Implement GraphQL query for organization ID resolution
- [x] 1.3 Add fallback to user ID query if organization not found
- [x] 1.4 Add error handling for invalid organization/user
- [x] 1.5 Add _create_project_v2(owner_id: str, title: str) -> str method
- [x] 1.6 Implement createProjectV2 GraphQL mutation
- [x] 1.7 Extract project number from created project URL/response
- [x] 1.8 Return project number and node ID
- [x] 1.9 Add error handling for insufficient permissions

## 2. Update GitHubProjectsTracker Initialization

- [x] 2.1 Make project_number optional in __init__ (default: None)
- [x] 2.2 Add auto_create parameter (default: True)
- [x] 2.3 Check if project_number is None and auto_create is True
- [x] 2.4 Call _get_owner_id() to resolve organization
- [x] 2.5 Generate project name with "Migration Agent - {org} - {timestamp}"
- [x] 2.6 Call _create_project_v2() to create project
- [x] 2.7 Store created project_number in instance variable
- [x] 2.8 Print project number and URL to console
- [x] 2.9 Suggest user add TRACKER_GITHUB_PROJECT_NUMBER to .env
- [x] 2.10 Fall back to LocalTracker if creation fails

## 3. Add Project Deletion Support

- [x] 3.1 Add delete_project(project_id: str) -> bool method
- [x] 3.2 Implement deleteProjectV2 GraphQL mutation
- [x] 3.3 Handle deletion errors gracefully
- [x] 3.4 Return True on success, False on failure
- [x] 3.5 Add logging for deletion operations

## 4. Update Configuration Validation

- [x] 4.1 Update _validate_github_config to make project_number optional
- [x] 4.2 Add validation for optional project_name field
- [x] 4.3 Add validation for optional project_description field
- [x] 4.4 Update error messages to reflect optional project_number
- [x] 4.5 Add warning if token might lack 'project' scope

## 5. Create Integration Test Infrastructure

- [x] 5.1 Create tests/integration/ directory
- [x] 5.2 Create tests/integration/__init__.py
- [x] 5.3 Create .env.test.example template file
- [x] 5.4 Document required test environment variables in .env.test.example
- [x] 5.5 Add .env.test to .gitignore
- [x] 5.6 Add setup instructions in .env.test.example header

## 6. Implement Integration Test Script

- [x] 6.1 Create tests/integration/test_github_integration.py
- [x] 6.2 Add function to load .env.test configuration
- [x] 6.3 Add function to validate required test environment variables
- [x] 6.4 Add function to check GitHub API rate limits before starting
- [x] 6.5 Implement test_create_project() - creates test project
- [x] 6.6 Implement test_create_items() - creates 3 test issues
- [ ] 6.7 Implement test_update_item_status() - changes status Backlog → In Progress → Done
- [x] 6.8 Implement test_verify_items() - validates items exist with correct fields
- [x] 6.9 Add cleanup function to delete test project
- [x] 6.10 Wrap tests in try/finally to ensure cleanup runs

## 7. Add Test Utilities

- [x] 7.1 Add generate_test_project_name() - creates unique name with timestamp
- [x] 7.2 Add wait_for_rate_limit() - waits if rate limit too low
- [x] 7.3 Add print_test_progress() - shows test step being executed
- [x] 7.4 Add assert_test() - custom assertion with helpful error messages
- [x] 7.5 Add get_rate_limit_status() - queries remaining API quota

## 8. Add Test Output and Reporting

- [ ] 8.1 Add colored output for pass/fail (green/red)
- [x] 8.2 Print created resource IDs and URLs during test
- [x] 8.3 Show summary at end (total tests, passed, failed)
- [ ] 8.4 Report API calls used during test
- [x] 8.5 Exit with code 0 on success, 1 on failure
- [x] 8.6 Add --json flag for machine-readable output
- [x] 8.7 Add --keep-project flag to skip cleanup for debugging

## 9. Update Documentation

- [x] 9.1 Update main README.md with project auto-creation section
- [x] 9.2 Document that project_number is now optional
- [x] 9.3 Add example of auto-creation workflow
- [x] 9.4 Update agents/project-tracker-agent/README.md
- [x] 9.5 Add "GitHub Project Auto-Creation" section
- [x] 9.6 Document how to run integration tests
- [x] 9.7 Add troubleshooting for project creation errors
- [x] 9.8 Document required GitHub token permissions for creation

## 10. Update .env.example

- [x] 10.1 Update .env.example to show project_number is optional
- [x] 10.2 Add comments explaining auto-creation behavior
- [x] 10.3 Add optional TRACKER_GITHUB_PROJECT_NAME variable
- [x] 10.4 Add optional TRACKER_GITHUB_PROJECT_DESCRIPTION variable
- [x] 10.5 Add comment about 'project' scope requirement

## 11. Add Unit Tests

- [x] 11.1 Add tests/test_github_tracker.py tests for _get_owner_id()
- [x] 11.2 Add tests for _create_project_v2() with mocked GraphQL
- [x] 11.3 Add tests for delete_project() with mocked GraphQL
- [x] 11.4 Add tests for auto-creation in __init__
- [x] 11.5 Add tests for fallback when creation fails
- [x] 11.6 Add tests for project_number None vs explicit

## 12. Testing and Validation

- [x] 12.1 Run unit tests and verify pass rate
- [ ] 12.2 Test auto-creation with real GitHub account
- [ ] 12.3 Test with explicit project_number (ensure no auto-create)
- [ ] 12.4 Run integration test script with .env.test
- [ ] 12.5 Verify cleanup removes test project
- [ ] 12.6 Test with insufficient permissions (verify graceful fallback)
- [ ] 12.7 Test with rate limit near zero (verify wait/skip)
- [ ] 12.8 Validate documentation examples work
- [ ] 12.9 Test both organization and user-level projects
- [x] 12.10 Verify auto-created project number is printed to console

## 13. GitHub Test Environment Documentation (ADDED)

- [x] 13.1 Create SETUP_TESTING.md with step-by-step setup guide
- [x] 13.2 Document personal account vs test organization options
- [x] 13.3 Create TEST_QUICK_REFERENCE.md for quick command reference
- [x] 13.4 Add test environment setup to TESTING.md
- [x] 13.5 Update .env.test.example with detailed setup instructions
- [x] 13.6 Add make verify-org command to verify organization access
- [x] 13.7 Add make test-setup-verify to verify complete setup
- [x] 13.8 Update Makefile help with test environment requirements
- [x] 13.9 Update README.md with test environment setup links
- [x] 13.10 Add troubleshooting for test environment setup issues

# Testing Guide - Project Tracker Agent

This guide covers how to test the project tracker agent, including unit tests and integration tests.

## Quick Start

```bash
# 1. Setup
make setup           # Install dependencies
make env-setup       # Create .env.test from template

# 2. Configure credentials
# Edit .env.test and add your GitHub credentials:
#   TRACKER_GITHUB_TOKEN=ghp_your_token_here
#   TRACKER_GITHUB_ORGANIZATION=your-org-or-username

# 3. Run tests
make test-integration
```

## Available Test Commands

### Integration Tests

```bash
# Run integration tests (creates/deletes real GitHub project)
make test-integration

# Run with JSON output (for CI/CD)
make test-integration-json

# Keep test project for debugging
make test-integration-keep

# Check if .env.test is configured
make env-check
```

### Unit Tests

```bash
# Run unit tests only (no GitHub API calls)
make test-unit

# Check Python syntax
make test-syntax
```

### All Tests

```bash
# Run both unit and integration tests
make test
```

### GitHub API Utilities

```bash
# Check GitHub API rate limit
make rate-limit

# Validate GitHub token and permissions
make validate-token
```

### Development Tools

```bash
# Install development dependencies (pytest, pylint, etc.)
make install-dev

# Format code with black
make format

# Run linter
make lint

# Clean up Python cache files
make clean
```

## Integration Test Configuration

The integration tests use `.env.test` for configuration:

### Required Variables

```bash
# GitHub Personal Access Token with 'project' and 'repo' scopes
TRACKER_GITHUB_TOKEN=ghp_your_token_here

# GitHub organization or username
TRACKER_GITHUB_ORGANIZATION=your-org-or-username
```

### Optional Variables

```bash
# Use existing project (WARNING: will modify it!)
TRACKER_GITHUB_PROJECT_NUMBER=5

# Custom project name for test projects
TRACKER_GITHUB_PROJECT_NAME=My Test Project

# Keep test project after tests complete
TEST_KEEP_PROJECT=false

# Minimum API rate limit to run tests
TEST_MIN_RATE_LIMIT=20
```

## What Integration Tests Do

1. **Create Project** - Creates a temporary GitHub Project
2. **Create Items** - Adds 3 test user stories
3. **Verify Items** - Validates items exist with correct fields
4. **List Items** - Tests item listing functionality
5. **Cleanup** - Deletes test project (unless `TEST_KEEP_PROJECT=true`)

## Test Output

### Success

```
======================================================================
  TEST: Create GitHub Project
======================================================================
✓ Created project #5: Migration Agent Test - my-org - 20260512-143022
  URL: https://github.com/orgs/my-org/projects/5

======================================================================
  TEST: Create Project Items
======================================================================
✓ Test passed: Created 3 items
  Item 1: PVTI_lADOABc...
  Item 2: PVTI_lADOABc...
  Item 3: PVTI_lADOABc...

======================================================================
  CLEANUP: Delete Test Project
======================================================================
✓ Cleanup complete: Project deleted

======================================================================
  TEST SUMMARY
======================================================================
Total tests: 5
Passed: 5
Failed: 0
======================================================================
```

### Failure

If tests fail, you'll see detailed error messages:

```
✗ Test failed: Failed to create project: ...
```

## Troubleshooting

### .env.test not found

```bash
make env-setup  # Creates .env.test from template
```

### TRACKER_GITHUB_TOKEN not configured

Edit `.env.test` and set your GitHub Personal Access Token:

```bash
TRACKER_GITHUB_TOKEN=ghp_your_token_here
```

Get a token at: https://github.com/settings/tokens

Required scopes:
- `project` - For creating/managing projects
- `repo` - For organization access

### Rate limit exceeded

Wait for rate limit to reset, or check remaining quota:

```bash
make rate-limit
```

Authenticated requests have 5000/hour limit.

### Invalid token or permissions

Validate your token:

```bash
make validate-token
```

Ensure token has `project` and `repo` scopes.

### Test project not cleaned up

If tests are interrupted, you may have orphaned test projects.

Test projects are named: `Migration Agent Test - {org} - {timestamp}`

Delete manually from GitHub: https://github.com/orgs/YOUR_ORG/projects

Or re-run with cleanup:

```bash
# Find project ID and delete via GraphQL API
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: make setup

      - name: Run integration tests
        run: make test-integration-json
        env:
          TRACKER_GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TRACKER_GITHUB_ORGANIZATION: ${{ github.repository_owner }}
```

### GitLab CI

```yaml
integration-tests:
  stage: test
  script:
    - make setup
    - make test-integration-json
  variables:
    TRACKER_GITHUB_TOKEN: $GITHUB_TOKEN
    TRACKER_GITHUB_ORGANIZATION: my-org
```

## Manual Testing

Run integration tests directly without Make:

```bash
# Create .env.test first
cp .env.test.example .env.test
# Edit .env.test with credentials

# Run tests
python tests/integration/test_github_integration.py

# JSON output
python tests/integration/test_github_integration.py --json
```

## Test Development

### Adding New Tests

1. Add test function to `tests/integration/test_github_integration.py`:

```python
def test_my_feature(tracker: GitHubProjectsTracker) -> None:
    """Test my new feature"""
    print_test_progress("TEST: My Feature")

    # Test implementation
    result = tracker.my_feature()

    assert_test(result is not None, "Result should not be None")

    print(f"\n✓ Test passed: My feature works")
```

2. Add test to `run_integration_tests()` sequence

3. Update test count in results dictionary

### Running Specific Tests

```bash
# Run with pytest (if installed)
python -m pytest tests/integration/test_github_integration.py::test_create_project -v

# Or modify the script to comment out unwanted tests
```

## Performance

Integration tests make ~10-15 GitHub API calls:

- Get owner ID: 1-2 calls
- Create project: 1 call
- Create items: 3 calls
- Verify items: 3 calls
- List items: 1 call
- Delete project: 1 call

Typical runtime: 10-30 seconds (depends on network latency)

## Security

**IMPORTANT:**

- ✅ `.env.test` is in `.gitignore` - never committed
- ✅ Credentials are loaded from environment only
- ✅ Test projects are automatically deleted
- ⚠️ Never commit tokens or credentials to version control
- ⚠️ Rotate tokens if accidentally exposed

## Best Practices

1. **Use dedicated test organization** - Don't test on production projects
2. **Check rate limit** - Run `make rate-limit` before large test runs
3. **Review .env.test** - Ensure credentials are not placeholder values
4. **Monitor test projects** - Verify cleanup is working
5. **Use TEST_KEEP_PROJECT=true** - When debugging test failures

## Additional Resources

- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub Projects v2](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

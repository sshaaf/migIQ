# Quick Setup Guide for Integration Testing

This guide walks you through setting up your test environment from scratch.

## Prerequisites

- GitHub account (free tier is fine)
- Command line access
- Python 3.7+ installed

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd agents/project-tracker-agent
make setup
```

**Expected output:**
```
Installing dependencies...
✓ Dependencies installed
```

---

### 2. Choose Your Test Environment

Pick one of these options:

#### Option A: Personal Account (Fastest)

**Use this if:**
- ✅ You want to start testing immediately
- ✅ You're okay with test projects in your personal account

**Your username is:**
- Visit https://github.com
- Look at the top-right profile icon - click it
- Your username is shown there (e.g., `octocat`)

**Continue to Step 3 using your username**

---

#### Option B: Test Organization (Recommended)

**Use this if:**
- ✅ You want isolated test environment
- ✅ You're setting up for a team or CI/CD

**Create test organization:**

1. Visit: https://github.com/organizations/new
2. Fill in:
   - **Account name:** `your-username-testing` (or any name you prefer)
   - **Contact email:** Your email
   - **Plan:** Free
3. Click "Create organization"
4. **Important:** Note your organization name for Step 3

**Continue to Step 3 using your organization name**

---

### 3. Create GitHub Personal Access Token

1. **Visit:** https://github.com/settings/tokens

2. **Click:** "Generate new token (classic)"

3. **Fill in:**
   - **Note:** `migration-agent-testing`
   - **Expiration:** 90 days (recommended)
   - **Select scopes:**
     - ✅ `repo` - Full control of private repositories
     - ✅ `project` - Full control of projects

4. **Click:** "Generate token"

5. **Copy the token** - it starts with `ghp_`

   ⚠️ **Save this token safely** - you won't see it again!

---

### 4. Configure .env.test

```bash
# Create .env.test from template
make env-setup
```

**Expected output:**
```
✓ Created .env.test from template
⚠ Remember to edit .env.test with your GitHub credentials
```

**Edit .env.test:**

```bash
# Open in your editor
nano .env.test
# or
vim .env.test
# or
code .env.test
```

**Replace these lines:**

```bash
# BEFORE (template values)
TRACKER_GITHUB_TOKEN=ghp_your_token_here
TRACKER_GITHUB_ORGANIZATION=your-org-or-username
TRACKER_GITHUB_PROJECT_NAME=My Integration Test Project

# AFTER (your actual values)
TRACKER_GITHUB_TOKEN=ghp_1234567890abcdef1234567890abcdef12345678
TRACKER_GITHUB_ORGANIZATION=your-username-testing
TRACKER_GITHUB_PROJECT_NAME=My Integration Test Project
```

**Save and close the file**

**Note on project naming:**
- `TRACKER_GITHUB_PROJECT_NAME` is **required** for integration tests
- Tests will fail with a validation error if this field is missing or empty
- Use a descriptive name to easily identify your test projects in GitHub UI
- Example: "My Integration Test Project" or "Testing Environment"

---

### 5. Verify Setup

```bash
make test-setup-verify
```

**Expected output:**
```
✓ .env.test is configured
Validating GitHub token...
✓ Token valid for user: your-username
Verifying GitHub organization access...
✓ Organization found: your-username-testing
  Type: Organization
  Public repos: 0
Checking GitHub API rate limit...
{
  "resources": {
    "graphql": {
      "limit": 5000,
      "remaining": 5000,
      ...
    }
  }
}

✓ Test environment setup verified!
  Ready to run integration tests
```

**If you see errors:**
- ❌ Token validation failed → Check your token in .env.test
- ❌ Organization not found → Check organization name spelling
- ❌ Rate limit too low → Wait for rate limit to reset

---

### 6. Run Integration Tests

```bash
make test-integration
```

**Expected output:**
```
Running integration tests...
This will make real API calls to GitHub

======================================================================
  TEST: Create GitHub Project
======================================================================
✓ Resolved owner ID: MDEyOk9yZ2FuaXphdGlvbjEyMzQ1Njc4
✓ Created project #1: Migration Agent Test - your-username-testing - 20260512-143022
  URL: https://github.com/orgs/your-username-testing/projects/1

✓ Test passed: Created project #1

======================================================================
  TEST: Create Project Items
======================================================================
✓ Created item TEST-001: PVTI_lADOABcD12MAAg
✓ Created item TEST-002: PVTI_lADOABcD12MABh
✓ Created item TEST-003: PVTI_lADOABcD12MACi

✓ Test passed: Created 3 items

======================================================================
  TEST: Verify Project Items
======================================================================
✓ Verified item PVTI_lADOABcD12MAAg: [TEST-001] Test Story 1
✓ Verified item PVTI_lADOABcD12MABh: [TEST-002] Test Story 2
✓ Verified item PVTI_lADOABcD12MACi: [TEST-003] Test Story 3

✓ Test passed: Verified 3 items

======================================================================
  TEST: List Project Items
======================================================================
✓ Listed 3 items

✓ Test passed: Listed 3 items

======================================================================
  CLEANUP: Delete Test Project
======================================================================
✓ Successfully deleted test project
✓ Cleanup complete: Project deleted

======================================================================
  TEST SUMMARY
======================================================================
Total tests: 5
Passed: 5
Failed: 0
======================================================================

✓ Integration tests passed
```

**🎉 Success!** Your test environment is working!

---

## Troubleshooting

### "Token validation failed"

**Problem:** GitHub token is invalid or expired

**Solution:**
1. Check token in .env.test starts with `ghp_`
2. Verify token hasn't expired
3. Create a new token at https://github.com/settings/tokens
4. Update TRACKER_GITHUB_TOKEN in .env.test

---

### "Organization not found"

**Problem:** Organization name is incorrect or doesn't exist

**Solutions:**

**If using personal account:**
```bash
# Visit https://github.com/YOUR_USERNAME
# Your username is in the URL - use that in .env.test
TRACKER_GITHUB_ORGANIZATION=YOUR_USERNAME
```

**If using organization:**
```bash
# Visit https://github.com/orgs/YOUR_ORG
# Your org name is in the URL - use that in .env.test
TRACKER_GITHUB_ORGANIZATION=YOUR_ORG
```

---

### "Permission denied" or "Not Found"

**Problem:** Token doesn't have required scopes

**Solution:**
1. Go to https://github.com/settings/tokens
2. Click on your token name
3. Verify these scopes are checked:
   - ✅ repo
   - ✅ project
4. If not, delete token and create new one with correct scopes

---

### "Rate limit exceeded"

**Problem:** Used too many API calls

**Solution:**
```bash
# Check when rate limit resets
make rate-limit

# Wait for reset time shown in output
# Or wait 1 hour for rate limit to reset
```

---

### Tests fail but no clear error

**Problem:** Network issues or API changes

**Solution:**
```bash
# Run with verbose output
python tests/integration/test_github_integration.py

# Or keep test project to inspect manually
make test-integration-keep

# Then check project at:
# https://github.com/orgs/YOUR_ORG/projects
```

---

## Next Steps

**Run tests regularly:**
```bash
make test-integration
```

**Use in CI/CD:**
```yaml
# .github/workflows/test.yml
- run: make test-integration-json
  env:
    TRACKER_GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TRACKER_GITHUB_ORGANIZATION: your-test-org
```

**Clean up:**
```bash
# If you have orphaned test projects, delete them at:
# https://github.com/orgs/YOUR_ORG/projects

# Look for projects named:
# "Migration Agent Test - YOUR_ORG - TIMESTAMP"
```

---

## Summary Checklist

- [ ] Installed dependencies (`make setup`)
- [ ] Created GitHub organization or using personal account
- [ ] Created Personal Access Token with `repo` and `project` scopes
- [ ] Created .env.test (`make env-setup`)
- [ ] Configured TRACKER_GITHUB_TOKEN in .env.test
- [ ] Configured TRACKER_GITHUB_ORGANIZATION in .env.test
- [ ] Configured TRACKER_GITHUB_PROJECT_NAME in .env.test
- [ ] Verified setup (`make test-setup-verify`)
- [ ] Ran integration tests (`make test-integration`)
- [ ] Tests passed ✅

---

## Help & Support

**More details:**
- Full testing guide: [TESTING.md](./TESTING.md)
- Tracker documentation: [README.md](./README.md)

**Common commands:**
```bash
make help                  # Show all available commands
make test-setup-verify     # Verify test environment
make test-integration      # Run integration tests
make rate-limit           # Check API rate limit
make validate-token       # Validate GitHub token
```

**Still stuck?**
- Check [TESTING.md](./TESTING.md) for detailed troubleshooting
- Review GitHub token scopes at https://github.com/settings/tokens
- Verify organization exists at https://github.com/orgs/YOUR_ORG

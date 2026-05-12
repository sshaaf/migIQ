# Integration Testing Quick Reference

## 🎯 I want to...

### Run integration tests
```bash
make test-integration
```

### Set up testing for the first time
**See:** [SETUP_TESTING.md](./SETUP_TESTING.md) (5-minute step-by-step guide)

**TL;DR:**
```bash
make setup && make env-setup
# Edit .env.test with GitHub credentials + project name (required)
make test-setup-verify
make test-integration
```

### Create a GitHub test environment

**Option 1: Personal Account** (2 minutes)
- Use your GitHub username
- Get token at: https://github.com/settings/tokens
- Scopes needed: `repo`, `project`

**Option 2: Test Organization** (5 minutes)
- Create at: https://github.com/organizations/new
- Name: `your-username-testing`
- Get token at: https://github.com/settings/tokens
- Scopes needed: `repo`, `project`

### Verify my setup is correct
```bash
make test-setup-verify
```

This checks:
- ✅ .env.test exists and is configured
- ✅ GitHub token is valid
- ✅ Organization/user exists and is accessible
- ✅ API rate limit is sufficient

### Check if I have enough API quota
```bash
make rate-limit
```

### Debug a failing test
```bash
# Keep test project to inspect manually
make test-integration-keep

# Then visit: https://github.com/orgs/YOUR_ORG/projects
```

### See all available test commands
```bash
make help
```

---

## 📋 Required Setup

| Requirement | Where to get it | Notes |
|-------------|----------------|-------|
| GitHub Account | https://github.com | Free tier is fine |
| GitHub Token | https://github.com/settings/tokens | Scopes: `repo`, `project` |
| GitHub Org/User | Your username OR https://github.com/organizations/new | Test org recommended |
| Project Name | **Required**: Set `TRACKER_GITHUB_PROJECT_NAME` in .env.test | Example: "My Integration Test Project" |

---

## 🚀 Quick Commands

| Command | What it does |
|---------|--------------|
| `make setup` | Install dependencies |
| `make env-setup` | Create .env.test template |
| `make test-setup-verify` | Verify everything is configured |
| `make test-integration` | Run integration tests |
| `make test-integration-json` | Run tests with JSON output (for CI/CD) |
| `make test-integration-keep` | Run tests but keep test project |
| `make rate-limit` | Check GitHub API rate limit |
| `make validate-token` | Verify GitHub token |
| `make verify-org` | Verify organization access |

---

## 🔧 Troubleshooting

| Error | Solution |
|-------|----------|
| "Token validation failed" | Check token in .env.test, create new at https://github.com/settings/tokens |
| "Organization not found" | Check spelling, verify org exists, or use personal username |
| "Permission denied" | Token needs `repo` and `project` scopes |
| "Rate limit exceeded" | Wait 1 hour or run `make rate-limit` to check reset time |
| ".env.test not found" | Run `make env-setup` |
| "TRACKER_GITHUB_PROJECT_NAME is required" | Edit .env.test and set: `TRACKER_GITHUB_PROJECT_NAME=My Test Project` |

---

## 📚 Documentation

- **[SETUP_TESTING.md](./SETUP_TESTING.md)** - Complete step-by-step setup guide (5 min read)
- **[TESTING.md](./TESTING.md)** - Comprehensive testing guide (15 min read)
- **[README.md](./README.md)** - Main documentation
- **Makefile** - Run `make help` to see all commands

---

## 💡 Tips

- **First time?** Follow [SETUP_TESTING.md](./SETUP_TESTING.md) step-by-step
- **Creating test org?** Name it `your-username-testing` for clarity
- **Token expires?** Create new one at https://github.com/settings/tokens
- **Tests fail?** Run `make test-setup-verify` to check setup
- **Need help?** See [TESTING.md](./TESTING.md) for detailed troubleshooting

---

## 🎓 What the tests do

1. ✅ Create temporary GitHub Project
2. ✅ Create 3 test user stories
3. ✅ Verify items exist with correct fields
4. ✅ List all project items
5. ✅ Delete test project (cleanup)

**Time:** ~10-30 seconds
**API calls:** ~15 calls (0.3% of 5000/hour limit)
**Cleanup:** Automatic (unless using `make test-integration-keep`)

---

## 🔐 Security

- ✅ `.env.test` is gitignored (never committed)
- ✅ Test projects auto-deleted after tests
- ⚠️ Never commit tokens to version control
- ⚠️ Rotate tokens if accidentally exposed

---

## 🤝 CI/CD Integration

**GitHub Actions:**
```yaml
- run: make test-integration-json
  env:
    TRACKER_GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TRACKER_GITHUB_ORGANIZATION: your-test-org
```

**GitLab CI:**
```yaml
test:
  script:
    - make test-integration-json
  variables:
    TRACKER_GITHUB_TOKEN: $GITHUB_TOKEN
    TRACKER_GITHUB_ORGANIZATION: your-test-org
```

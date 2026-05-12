# Test Scripts

Helper scripts for integration testing and GitHub validation.

## Scripts

### validate_github_token.py

Validates a GitHub Personal Access Token.

**Usage:**
```bash
python3 scripts/validate_github_token.py <token>
```

**Example:**
```bash
python3 scripts/validate_github_token.py ghp_1234567890abcdef
```

**Exit codes:**
- `0` - Token is valid
- `1` - Token is invalid or error occurred

**Output:**
```
✓ Token valid for user: octocat
```

---

### verify_github_org.py

Verifies a GitHub organization or user exists and is accessible.

**Usage:**
```bash
python3 scripts/verify_github_org.py <token> <org_or_username>
```

**Example:**
```bash
python3 scripts/verify_github_org.py ghp_1234567890abcdef my-org
```

**Exit codes:**
- `0` - Organization or user found
- `1` - Not found or error occurred

**Output (organization):**
```
✓ Organization found: my-org
  Type: Organization
  Public repos: 42
```

**Output (user fallback):**
```
⚠ Not an organization - trying as user account...
✓ User account found: octocat
  Type: User
  Public repos: 15
```

**Output (not found):**
```
⚠ Not an organization - trying as user account...
✗ Neither organization nor user found
  Check TRACKER_GITHUB_ORGANIZATION in .env.test
  Tried: nonexistent-org
```

---

## Used By

These scripts are used by the Makefile targets:

- `make validate-token` - Uses `validate_github_token.py`
- `make verify-org` - Uses `verify_github_org.py`
- `make test-setup-verify` - Uses both scripts

---

## Development

**Test validate_github_token.py:**
```bash
# With valid token
export GITHUB_TOKEN=ghp_your_token_here
python3 scripts/validate_github_token.py "$GITHUB_TOKEN"

# With invalid token
python3 scripts/validate_github_token.py "invalid_token"
```

**Test verify_github_org.py:**
```bash
# Test with organization
python3 scripts/verify_github_org.py "$GITHUB_TOKEN" "github"

# Test with user account
python3 scripts/verify_github_org.py "$GITHUB_TOKEN" "octocat"

# Test with nonexistent
python3 scripts/verify_github_org.py "$GITHUB_TOKEN" "nonexistent-12345"
```

---

## Why Separate Scripts?

Originally, these were inline Python code in the Makefile, but:

❌ **Problems with inline Python:**
- Hard to debug syntax errors
- Complex escaping of quotes and special characters
- Poor error messages
- Difficult to test independently

✅ **Benefits of separate scripts:**
- Easier to debug and test
- Better error messages
- Can be run independently
- Cleaner Makefile
- Standard Python error handling

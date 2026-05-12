## Context

Currently, configuration for tracker integrations and agents is passed via JSON in command-line arguments:
```bash
python3 project_tracker.py --context '{"tracker":{"type":"github","config":{"token":"$GITHUB_TOKEN",...}}}'
```

This approach has limitations:
- Verbose and error-prone for users
- Credentials visible in process lists and shell history
- Difficult to version control configuration examples
- No clear reference for available configuration options
- Environment variable substitution ($VAR) happens in config.py, not at shell level

Industry standard for configuration management uses .env files with libraries like python-dotenv. This provides:
- One place for all configuration
- .env.example for documentation
- .gitignore .env for security
- Simple key=value syntax

Constraints:
- Must maintain backward compatibility with existing JSON context approach
- Must work with existing environment variable resolution ($GITHUB_TOKEN)
- Should not require .env file to be present (fallback to context)

## Goals / Non-Goals

**Goals:**
- Load configuration from .env file using python-dotenv library
- Provide comprehensive .env.example with all configuration options documented
- Map flat environment variables to nested config structure (TRACKER_TYPE → tracker.type)
- Maintain backward compatibility with JSON context configuration
- Add .env to .gitignore automatically
- Update all documentation to recommend .env as primary configuration method

**Non-Goals:**
- Replace all environment variable usage (PATH, HOME, etc. remain system-level)
- Implement configuration validation beyond what already exists
- Add configuration hot-reloading or watch functionality
- Support multiple .env files or environments (.env.dev, .env.prod) in initial version

## Decisions

### D1: Use python-dotenv Library

**Decision:** Use python-dotenv for .env file parsing

**Rationale:**
- Industry standard, 15K+ GitHub stars, widely used
- Simple API: `load_dotenv()` loads .env into os.environ
- Handles comments, multiline values, quotes
- Zero configuration needed
- MIT licensed

**Alternatives considered:**
- Manual .env parsing → Rejected: reinventing wheel, edge cases (quotes, escapes, multiline)
- python-decouple → Rejected: more opinionated, less widely adopted
- configparser (INI format) → Rejected: .env is more standard for credentials

### D2: Environment Variable Naming Convention

**Decision:** Use uppercase, underscore-separated, prefixed naming:
```
TRACKER_TYPE=github
TRACKER_GITHUB_TOKEN=$GITHUB_TOKEN
TRACKER_GITHUB_ORGANIZATION=my-org
TRACKER_GITHUB_PROJECT_NUMBER=5
```

**Rationale:**
- Follows Unix environment variable conventions (uppercase)
- Prefixing (TRACKER_*) prevents collisions with system variables
- Nested structure maps naturally to config dict

**Alternatives considered:**
- Dotted notation (tracker.type) → Rejected: not valid in bash
- No prefixes → Rejected: collision risk (TYPE, TOKEN too generic)
- JSON in single env var → Rejected: defeats purpose of .env simplicity

### D3: Configuration Loading Priority

**Decision:** Load in this order (first wins):
1. Explicit JSON context (--context argument)
2. Environment variables from .env file
3. System environment variables
4. Default values

**Rationale:**
- Explicit context overrides all (backward compatibility, explicit intent)
- .env file is primary new method
- System env vars provide flexibility for CI/CD
- Defaults ensure graceful degradation

**Alternatives considered:**
- .env overrides context → Rejected: breaks backward compatibility
- Only .env or context (not both) → Rejected: too restrictive
- .env required → Rejected: breaks existing deployments

### D4: Configuration Mapper Function

**Decision:** Create `load_config_from_env()` function that:
- Calls `load_dotenv()` to load .env file
- Maps environment variables to nested dict structure
- Returns config dict compatible with existing code

**Rationale:**
- Centralized mapping logic
- Reusable across agents
- Clean separation: dotenv loading vs. config mapping

### D5: .env.example Structure

**Decision:** Organize .env.example by component with inline comments:
```
# Tracker Configuration
TRACKER_TYPE=local
# TRACKER_GITHUB_TOKEN=ghp_your_token_here
# TRACKER_GITHUB_ORGANIZATION=your-org
```

**Rationale:**
- Commented-out examples prevent accidental usage
- Inline comments provide context
- Grouped by component for discoverability

## Risks / Trade-offs

**[Risk]** Users forget to create .env from .env.example and get confusing errors
→ **Mitigation:** Check for .env.example but not .env on startup, print helpful message

**[Risk]** .env file accidentally committed with credentials
→ **Mitigation:** Add .env to .gitignore in project template, document in README

**[Risk]** Confusion about environment variable priority (system vs .env vs context)
→ **Mitigation:** Document priority clearly in .env.example and README

**[Trade-off]** Adding python-dotenv dependency
→ **Accepted:** Small (~10KB), widely used, provides significant UX improvement

**[Risk]** Environment variable names become very long (TRACKER_GITHUB_ORGANIZATION)
→ **Mitigation:** Document abbreviations are acceptable, provide clear examples

**[Trade-off]** Flat .env structure vs nested JSON loses some expressiveness
→ **Accepted:** Most config is simple key-value, complex structures can still use JSON context

## Migration Plan

**Phase 1: Add dotenv Support**
1. Add python-dotenv to requirements
2. Create .env.example with all options
3. Add .env to .gitignore
4. Implement `load_config_from_env()` function
5. Update ProjectTrackerAgent to try .env loading

**Phase 2: Update Documentation**
1. Update README with .env configuration examples
2. Update project-tracker-agent README
3. Add "Getting Started" section showing .env setup

**Phase 3: Validation**
1. Test with .env file present
2. Test without .env file (backward compatibility)
3. Test with partial .env (mixed with context)
4. Test environment variable priority

**Rollback Strategy:**
- .env loading is additive, doesn't break existing functionality
- If issues found, can simply not create .env file
- No database migrations or data changes
- Can remove dotenv import and fall back to context-only

**Deployment:**
- Update existing deployments by creating .env from current context JSON
- Provide migration script to convert context JSON to .env format
- Gradual adoption: .env is opt-in, context continues to work

## Open Questions

1. Should we support .env.local for local overrides?
   - Leaning **no** for initial version, can add later

2. Should we validate required vs optional env vars at startup?
   - Leaning **yes** - print warning for missing required vars with .env.example reference

3. Should .env.example be tracked in git?
   - **Yes** - it's documentation, not credentials

4. Should we auto-create .env from .env.example on first run?
   - Leaning **no** - too magical, user should explicitly create and configure

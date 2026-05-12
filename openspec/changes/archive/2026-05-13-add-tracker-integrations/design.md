## Context

The project tracker agent currently hard-codes task management to a local tasks.md file. The `TasksFileManager` class handles all task CRUD operations directly with markdown parsing/writing. Teams using GitHub Projects, GitLab Issues, or Jira need the agent to sync migration tasks with their existing project management tools.

Current state:
- `TasksFileManager` tightly coupled to markdown format
- Simulated Kanban integration in `_simulate_generate_backlog()` that doesn't actually call APIs
- No abstraction for different tracker backends
- Configuration only supports limited `kanban.platform` field with no credentials

Constraints:
- Must maintain backward compatibility with local tasks.md workflow
- GitHub Projects uses GraphQL API (v2), not REST
- Must avoid storing credentials in code or git
- Should support both authenticated and unauthenticated workflows (local doesn't need auth)

## Goals / Non-Goals

**Goals:**
- Create tracker abstraction layer that supports multiple backends
- Implement working GitHub Projects integration with full CRUD operations
- Maintain tasks.md as default tracker (no breaking changes)
- Support configuration via context dictionary passed from /migration skill
- Enable future GitLab and Jira integrations through same interface

**Non-Goals:**
- Two-way sync (tracker → tasks.md bidirectional updates)
- Real-time webhooks or event-driven sync
- GitLab or Jira implementation (design for extensibility only)
- UI for configuring trackers (CLI/config only)
- Conflict resolution for concurrent edits

## Decisions

### D1: Abstract Tracker Interface

**Decision:** Create `TrackerInterface` base class with methods: `create_issue()`, `update_issue()`, `get_issue()`, `list_issues()`, `sync_story()`

**Rationale:**
- Enables pluggable tracker implementations
- Isolates tracker-specific logic from agent orchestration
- Simplifies testing with mock trackers

**Alternatives considered:**
- Keep concrete implementations without interface → Rejected: leads to tight coupling, harder to test
- Use protocol/duck typing → Rejected: Python ABC provides better documentation and type safety

### D2: GitHub Projects via GraphQL

**Decision:** Use GitHub Projects v2 GraphQL API with `requests` library

**Rationale:**
- Projects v2 is the current GitHub Projects implementation
- GraphQL provides precise field selection and efficient queries
- `requests` is already a common dependency, avoids heavy PyGithub library

**Alternatives considered:**
- GitHub REST API → Rejected: Projects v2 not available in REST
- PyGithub library → Rejected: doesn't support Projects v2 GraphQL, adds large dependency
- octokit.py → Considered: good support but adds dependency overhead

### D3: Configuration via Context Dictionary

**Decision:** Extend existing context dict with tracker configuration:
```python
{
  "tracker": {
    "type": "github",  # or "local", "gitlab", "jira"
    "config": {
      "token": "$GITHUB_TOKEN",  # env var reference
      "organization": "my-org",
      "project_number": 5
    }
  }
}
```

**Rationale:**
- Consistent with existing context pattern
- Supports environment variable references for secrets
- Easy to extend per-tracker configurations

**Alternatives considered:**
- Separate config file → Rejected: adds complexity, context already centralized
- Hard-coded credentials → Rejected: security risk
- OAuth flow → Rejected: overkill for CLI agent, PAT tokens sufficient

### D4: Tasks.md as Single Source of Truth

**Decision:** Keep tasks.md as primary storage, tracker is sync target (one-way: tasks.md → tracker)

**Rationale:**
- Tasks.md provides durable, version-controlled record
- Avoids complex bidirectional sync logic
- Tracker can be changed/reset without data loss

**Alternatives considered:**
- Tracker as source of truth → Rejected: loses git history, vendor lock-in
- Bidirectional sync → Rejected: complex conflict resolution, out of scope

### D5: Tracker Factory Pattern

**Decision:** Use factory method `create_tracker(config)` that returns appropriate tracker instance based on config.type

**Rationale:**
- Clean instantiation point
- Easy to extend with new tracker types
- Centralizes tracker selection logic

## Risks / Trade-offs

**[Risk]** GitHub API rate limits (5000/hour authenticated, 60/hour unauthenticated)
→ **Mitigation:** Use authenticated requests, batch operations where possible, implement backoff/retry

**[Risk]** GitHub token security exposure in logs or errors
→ **Mitigation:** Read from env vars, sanitize error messages, never log tokens

**[Risk]** GraphQL query complexity limits
→ **Mitigation:** Keep queries simple, paginate results, monitor query costs

**[Trade-off]** One-way sync means tracker updates don't flow back to tasks.md
→ **Accepted:** Simplifies implementation, tasks.md remains authoritative

**[Trade-off]** Each tracker has different field mappings (story points, priority, etc.)
→ **Accepted:** Document mapping per tracker, implement best-effort field sync

**[Risk]** Network failures during tracker sync could leave inconsistent state
→ **Mitigation:** Log all sync operations, provide retry mechanism, fail gracefully

## Migration Plan

**Phase 1: Refactor Existing Code**
1. Extract `TrackerInterface` base class
2. Create `LocalTracker` wrapping existing `TasksFileManager` logic
3. Update `ProjectTrackerAgent` to use tracker interface
4. Add factory method `create_tracker()`
5. Update tests to work with new abstraction

**Phase 2: Implement GitHub Integration**
1. Create `GitHubProjectsTracker` class
2. Implement GraphQL mutation for creating issues
3. Implement status update mutations
4. Add field mapping (priority, story points, etc.)
5. Add authentication and error handling

**Phase 3: Update Configuration**
1. Extend context schema with tracker configuration
2. Add environment variable resolver
3. Update /migration skill to accept tracker config
4. Document configuration examples

**Rollback Strategy:**
- New tracker config is optional; if absent, defaults to LocalTracker (tasks.md only)
- No database migrations required
- Can disable tracker sync by setting `type: "local"` in config

**Deployment:**
- No infrastructure changes required
- Users opt-in by providing tracker configuration
- Existing workflows unchanged

## Open Questions

1. Should we support multiple trackers simultaneously (e.g., tasks.md + GitHub)?
   - Leaning **yes** for future, but implement single tracker first

2. How to handle GitHub project field customization (custom fields)?
   - Start with standard fields, document extension pattern for later

3. Should tracker sync be synchronous or async?
   - **Synchronous** for v1, consider async if performance issues arise

4. Error handling: fail fast or continue on tracker errors?
   - **Continue on tracker errors**, log warnings, migration should not block on sync failures

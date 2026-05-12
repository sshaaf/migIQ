## Context

Currently, users must invoke migrations with explicit command-line arguments like `/migration --project-path ./your-app --migration-type framework --target Quarkus`. This creates friction and requires users to understand the command structure upfront.

The goal is to enable natural language interaction where users can say "Migrate this app to Quarkus" and the system automatically:
1. Parses the migration intent
2. Detects the project path from current directory
3. Validates the source code exists
4. Constructs and runs the equivalent migration command

Current system components:
- `story-orchestrator-agent`: Receives commands and coordinates harness execution
- `.env` configuration: Stores project and tracker settings
- Agent mesh: Executes migration through test → code → benchmark → evaluation → CI harnesses

## Goals / Non-Goals

**Goals:**
- Enable natural language migration requests ("Migrate to X")
- Auto-detect project path from current working directory
- Validate project source exists before starting migration
- Maintain backward compatibility with explicit `/migration` commands
- Clear error messages when project cannot be detected or intent is ambiguous

**Non-Goals:**
- AI-powered framework recommendation (user must specify target)
- Automatic dependency resolution or conflict fixing (migration execution handles this)
- Cross-language migrations (still focused on Java ecosystem)
- Cloud deployment or infrastructure changes (migration scope only)

## Decisions

### Decision 1: Parser Architecture - Regex patterns vs LLM extraction

**Choice**: Use regex/keyword patterns with LLM fallback

**Rationale**:
- Common patterns are predictable ("Migrate to X", "Convert to Y", "Upgrade to Z")
- Regex is fast and deterministic for 80% case
- LLM extraction for ambiguous cases provides flexibility without latency overhead on simple requests
- Avoids external API dependency for basic cases

**Alternatives considered**:
- Pure LLM: Too slow and adds API dependency
- Pure regex: Too brittle for variant phrasings

### Decision 2: Project Detection Strategy - Walk up tree vs fixed depth

**Choice**: Walk up directory tree until project marker found or filesystem root

**Rationale**:
- Users often run commands from subdirectories (e.g., `src/main/java`)
- Maven/Gradle projects have clear markers (pom.xml, build.gradle)
- Consistent with how git finds .git directory
- Stops at filesystem root to avoid infinite loops

**Alternatives considered**:
- Fixed depth (3 levels up): Arbitrary limit, could fail in deep structures
- Only current directory: Requires users to always be in project root

### Decision 3: Context Building - Eager vs lazy loading

**Choice**: Lazy load project metadata, eager validate existence

**Rationale**:
- Validate source exists immediately (fast failure)
- Load full project metadata only if validation passes (avoids wasted work)
- Project analysis can be expensive (dependency tree, file scanning)
- Migration workflow needs full context, so load during orchestrator setup

**Alternatives considered**:
- Eager load everything: Wasteful if validation fails
- Fully lazy: Delays errors until deep in execution

### Decision 4: User Confirmation - Always ask vs mode-based

**Choice**: Ask for confirmation in interactive mode, skip in autonomous mode

**Rationale**:
- Interactive mode (default): Safety net for auto-detection errors
- Autonomous mode: Trusts auto-detection for CI/CD pipelines
- Consistent with existing MODE=interactive|autonomous setting
- Explicit `/migration` command skips confirmation (user already explicit)

**Alternatives considered**:
- Always confirm: Annoying in automation
- Never confirm: Risky if auto-detection is wrong

## Risks / Trade-offs

### Risk: Project detection false positives
**Scenario**: Detecting parent project instead of intended sub-module

**Mitigation**:
- Prefer deepest project marker (e.g., if both parent pom.xml and child pom.xml exist, use child)
- Display detected path prominently in confirmation
- Allow --project-path override

### Risk: Natural language parsing ambiguity
**Scenario**: "Migrate to Spring" could mean Spring Framework or Spring Boot

**Mitigation**:
- Require specific targets in supported frameworks list
- Ask for clarification when ambiguous
- Log equivalent command so user can learn explicit syntax

### Risk: Multi-module projects
**Scenario**: Maven/Gradle project with multiple sub-modules

**Mitigation**:
- Detect parent pom.xml / settings.gradle as project root
- Include all modules in migration scope
- Future: Allow scope restriction via natural language ("only auth module")

### Trade-off: Reduced explicitness
**Impact**: Users may not understand what command is actually running

**Mitigation**:
- Always display equivalent `/migration` command
- Log full command with all parameters
- Provide --dry-run mode to see what would be executed

## Migration Plan

**Implementation phases**:
1. Create parser module (standalone, testable)
2. Create project detector module (standalone, testable)
3. Create context builder (integrates parser + detector)
4. Update story-orchestrator-agent to invoke context builder
5. Add confirmation prompt to orchestrator
6. Update documentation with examples

**Rollout**:
- No breaking changes - explicit commands still work
- Feature flag: `ENABLE_NL_MIGRATION=true` (default: true)
- If disabled, fall back to requiring explicit `/migration` command

**Rollback**:
- Set `ENABLE_NL_MIGRATION=false` to disable feature
- No data migration needed (stateless feature)

## Open Questions

1. **Framework detection**: Should we auto-detect current framework from source code?
   - **Current**: User must know current state
   - **Proposed**: Detect Java EE, Spring, etc. from dependencies
   - **Decision needed**: Implementation priority

2. **Scope specification**: How should users limit migration scope to specific modules?
   - **Current**: Migrate entire project
   - **Proposed**: "Migrate only auth module to Quarkus"
   - **Decision needed**: Parsing complexity vs value

3. **Confirmation UX**: Terminal prompt vs web UI?
   - **Current**: Terminal only
   - **Future**: Could integrate with VS Code extension UI
   - **Decision needed**: After terminal implementation proves value

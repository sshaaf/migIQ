## Why

Users currently need to remember and type complex commands like `/migration --project-path ./your-app --migration-type framework` to start a migration. This creates friction and slows down the developer experience. Users should be able to express their intent naturally (e.g., "Migrate this app to Quarkus") and the system should intelligently detect the project context, validate prerequisites, and initiate the migration workflow automatically.

## What Changes

- Add natural language migration intent detection to parse user requests like "Migrate this app to Quarkus" or "Convert to Spring Boot"
- Implement automatic project path detection from the current working directory
- Add source code validation to ensure the project exists before initiating migration
- Create a migration context parser that extracts migration type (framework, dependency, etc.) from natural language
- Modify the orchestrator to accept simplified input and internally construct the full migration command
- Make the explicit `/migration` command optional - run it automatically in the background when natural language intent is detected
- Add clear error messages when project source is not found or context is ambiguous

## Capabilities

### New Capabilities
- `natural-language-migration-parser`: Parses natural language migration requests and extracts intent (target framework, migration type)
- `auto-project-detection`: Automatically detects project path from current working directory and validates source code exists
- `migration-context-builder`: Builds migration context from detected project and parsed intent

### Modified Capabilities
- `agent-mesh-orchestration`: Update story orchestrator to accept simplified natural language input and auto-construct migration commands

## Impact

**Affected Components:**
- `story-orchestrator-agent`: Needs to handle natural language input and auto-detect context
- User interface/CLI: Simplified command invocation
- Configuration system: May need to infer configuration from project structure

**Developer Experience:**
- Dramatically simplified: "Migrate this app to Quarkus" instead of multi-flag commands
- Faster iteration: Auto-detection eliminates manual path specification
- Better error handling: Clear validation feedback when source is missing

**Breaking Changes:**
- None - this is additive, explicit commands still work

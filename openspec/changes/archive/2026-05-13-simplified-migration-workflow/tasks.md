## 1. Create Natural Language Migration Parser

- [ ] 1.1 Create `agents/shared/nl_migration_parser.py` module
- [ ] 1.2 Implement regex patterns for common migration phrases ("Migrate to X", "Convert to Y", "Upgrade to Z")
- [ ] 1.3 Add framework name extraction with case-insensitive matching
- [ ] 1.4 Implement migration type detection (framework, dependency, data, api)
- [ ] 1.5 Add version constraint extraction (e.g., "Quarkus 3.x" → version="3.x")
- [ ] 1.6 Implement scope extraction for module-specific migrations
- [ ] 1.7 Add LLM fallback for ambiguous requests using Claude API
- [ ] 1.8 Create supported frameworks list (Quarkus, Spring Boot, Micronaut, etc.)
- [ ] 1.9 Implement validation against supported frameworks
- [ ] 1.10 Add error messages for unsupported or ambiguous requests
- [ ] 1.11 Create unit tests for parser with various phrasings
- [ ] 1.12 Test edge cases (empty input, gibberish, multiple targets)

## 2. Create Auto Project Detection

- [ ] 2.1 Create `agents/shared/project_detector.py` module
- [ ] 2.2 Implement walk-up-tree algorithm to find project root
- [ ] 2.3 Add project marker detection (pom.xml, build.gradle, build.gradle.kts, package.json)
- [ ] 2.4 Implement preference order (deepest project marker wins)
- [ ] 2.5 Add filesystem root detection to prevent infinite loops
- [ ] 2.6 Implement source code validation (check for src/ directory)
- [ ] 2.7 Add .java file existence check in source directories
- [ ] 2.8 Implement Maven project metadata extraction (groupId, artifactId, version)
- [ ] 2.9 Implement Gradle project metadata extraction
- [ ] 2.10 Add multi-module project detection
- [ ] 2.11 Create clear error messages when no source found
- [ ] 2.12 Add project summary display function
- [ ] 2.13 Create unit tests for various project structures
- [ ] 2.14 Test multi-module Maven projects
- [ ] 2.15 Test Gradle projects with subprojects
- [ ] 2.16 Test running from subdirectories

## 3. Create Migration Context Builder

- [ ] 3.1 Create `agents/shared/migration_context.py` module
- [ ] 3.2 Define MigrationContext dataclass with all required fields
- [ ] 3.3 Implement combine function (parser output + detector output → context)
- [ ] 3.4 Add validation for required fields (project_path, migration_type, target)
- [ ] 3.5 Implement equivalent command generation (/migration --project-path X --migration-type Y)
- [ ] 3.6 Add current framework detection from dependencies
- [ ] 3.7 Implement migration scope estimation (file count, dependency count)
- [ ] 3.8 Add warnings detection for incompatible patterns
- [ ] 3.9 Create context serialization for logging
- [ ] 3.10 Implement user override handling (--project-path flag takes precedence)
- [ ] 3.11 Create unit tests for context building
- [ ] 3.12 Test validation logic with incomplete contexts

## 4. Update Story Orchestrator Agent

- [ ] 4.1 Read current `agents/story-orchestrator-agent/agent.md` to understand structure
- [ ] 4.2 Add natural language detection in orchestrator input handling
- [ ] 4.3 Import nl_migration_parser module
- [ ] 4.4 Import project_detector module
- [ ] 4.5 Import migration_context module
- [ ] 4.6 Implement input type detection (natural language vs explicit command)
- [ ] 4.7 Add natural language parsing workflow
- [ ] 4.8 Add project auto-detection workflow
- [ ] 4.9 Add context building workflow
- [ ] 4.10 Implement context validation before proceeding
- [ ] 4.11 Add confirmation prompt display in interactive mode
- [ ] 4.12 Implement confirmation handling (proceed/abort)
- [ ] 4.13 Add MODE check to skip confirmation in autonomous mode
- [ ] 4.14 Display equivalent /migration command to user
- [ ] 4.15 Log complete command with all parameters
- [ ] 4.16 Add ENABLE_NL_MIGRATION feature flag check
- [ ] 4.17 Implement fallback to explicit command mode when flag is false
- [ ] 4.18 Update orchestrator documentation with new workflow

## 5. Add Configuration Support

- [ ] 5.1 Add ENABLE_NL_MIGRATION to .env.example (default: true)
- [ ] 5.2 Update configuration loader to read ENABLE_NL_MIGRATION
- [ ] 5.3 Document feature flag in README
- [ ] 5.4 Add rollback instructions (set flag to false)

## 6. Error Handling and User Feedback

- [ ] 6.1 Create error message templates for common failures
- [ ] 6.2 Implement "project not found" error with helpful suggestions
- [ ] 6.3 Implement "ambiguous intent" error with clarification prompt
- [ ] 6.4 Implement "unsupported framework" error with supported list
- [ ] 6.5 Add did-you-mean suggestions for misspelled frameworks
- [ ] 6.6 Create context display formatting for confirmation screen
- [ ] 6.7 Add color coding for different context fields (if terminal supports)
- [ ] 6.8 Implement verbose logging mode for debugging

## 7. Integration Testing

- [ ] 7.1 Create test project structure in tests/fixtures/
- [ ] 7.2 Create test Maven project with pom.xml
- [ ] 7.3 Create test Gradle project with build.gradle
- [ ] 7.4 Create multi-module Maven test project
- [ ] 7.5 Write integration test: "Migrate this app to Quarkus" from project root
- [ ] 7.6 Write integration test: Run from subdirectory (src/main/java)
- [ ] 7.7 Write integration test: Missing project source (empty directory)
- [ ] 7.8 Write integration test: Ambiguous request without target
- [ ] 7.9 Write integration test: Unsupported framework request
- [ ] 7.10 Write integration test: Explicit --project-path override
- [ ] 7.11 Write integration test: Autonomous mode (skip confirmation)
- [ ] 7.12 Write integration test: Feature flag disabled
- [ ] 7.13 Run all integration tests and verify pass

## 8. Documentation

- [ ] 8.1 Update README.md with natural language examples
- [ ] 8.2 Add "Quick Start" section with simple example
- [ ] 8.3 Document supported frameworks list
- [ ] 8.4 Add examples of different migration phrasings
- [ ] 8.5 Document project detection behavior
- [ ] 8.6 Add troubleshooting section for detection issues
- [ ] 8.7 Document ENABLE_NL_MIGRATION feature flag
- [ ] 8.8 Add comparison table: natural language vs explicit commands
- [ ] 8.9 Update agent documentation with new workflow
- [ ] 8.10 Add examples to install-local.sh output message

## 9. Validation and Polish

- [ ] 9.1 Test end-to-end: "Migrate to Spring Boot" from real Java project
- [ ] 9.2 Test end-to-end: "Convert to Quarkus" from subdirectory
- [ ] 9.3 Verify error messages are clear and actionable
- [ ] 9.4 Verify confirmation prompt displays correctly
- [ ] 9.5 Verify equivalent command is logged correctly
- [ ] 9.6 Test with ENABLE_NL_MIGRATION=false (fallback mode)
- [ ] 9.7 Test with MODE=autonomous (skip confirmation)
- [ ] 9.8 Run all unit tests and verify 100% pass
- [ ] 9.9 Run all integration tests and verify pass
- [ ] 9.10 Update CHANGELOG or release notes

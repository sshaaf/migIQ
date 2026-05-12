## 1. Add python-dotenv Dependency

- [x] 1.1 Create requirements.txt if it doesn't exist in project root
- [x] 1.2 Add python-dotenv>=1.0.0 to requirements.txt
- [x] 1.3 Add installation instructions to README.md

## 2. Create .env.example Template

- [x] 2.1 Create .env.example file in project root
- [x] 2.2 Add header with setup instructions and security warning
- [x] 2.3 Add "# General Configuration" section with SESSION_ID, MODE variables
- [x] 2.4 Add "# Tracker Configuration" section with TRACKER_TYPE
- [x] 2.5 Add "# Local Tracker" subsection with TRACKER_LOCAL_TASKS_PATH
- [x] 2.6 Add "# GitHub Tracker" subsection with TRACKER_GITHUB_* variables
- [x] 2.7 Add "# GitLab Tracker (Planned)" subsection with placeholder
- [x] 2.8 Add "# Jira Tracker (Planned)" subsection with placeholder
- [x] 2.9 Add inline comments explaining each variable's purpose
- [x] 2.10 Comment out sensitive variables (tokens, credentials)
- [x] 2.11 Provide safe default values for non-sensitive variables

## 3. Update .gitignore

- [x] 3.1 Create .gitignore if it doesn't exist
- [x] 3.2 Add .env to .gitignore
- [x] 3.3 Add .env.local to .gitignore
- [x] 3.4 Ensure .env.example is NOT in .gitignore

## 4. Implement Environment Variable Mapper

- [x] 4.1 Create trackers/env_mapper.py module
- [x] 4.2 Implement parse_bool(value: str) -> bool helper function
- [x] 4.3 Implement parse_int(value: str) -> int helper function
- [x] 4.4 Implement parse_list(value: str) -> List[str] helper function
- [x] 4.5 Implement map_env_to_config(prefix: str) -> Dict function
- [x] 4.6 Add logic to convert UPPER_CASE to nested lowercase dict keys
- [x] 4.7 Add logic to parse values by type (int, bool, list)
- [x] 4.8 Add logic to handle missing/empty environment variables
- [x] 4.9 Implement load_config_from_env(prefix: str = 'TRACKER') -> Dict

## 5. Update Configuration Module

- [x] 5.1 Import python-dotenv in trackers/config.py
- [x] 5.2 Import env_mapper functions
- [x] 5.3 Update validate_tracker_config to accept env-loaded config
- [x] 5.4 Add load_tracker_config_from_env() function
- [x] 5.5 Add merge_configs(env_config: Dict, context_config: Dict) -> Dict
- [x] 5.6 Add logic to prioritize context over environment
- [x] 5.7 Add helpful error messages for misconfigured environment variables

## 6. Update Project Tracker Agent

- [x] 6.1 Import load_dotenv in project_tracker.py
- [x] 6.2 Call load_dotenv() at module level or in __init__
- [x] 6.3 Import load_tracker_config_from_env in project_tracker.py
- [x] 6.4 Update ProjectTrackerAgent.__init__ to load config from environment
- [x] 6.5 Add logic to merge environment config with context config
- [x] 6.6 Add logging to indicate config source (env, context, or merged)
- [x] 6.7 Check for .env.example and print helpful message if .env missing
- [x] 6.8 Support loading .env.local for local overrides

## 7. Add Tests

- [x] 7.1 Create tests/test_env_mapper.py
- [x] 7.2 Add test for parse_bool with various inputs
- [x] 7.3 Add test for parse_int with valid and invalid inputs
- [x] 7.4 Add test for parse_list with comma-separated values
- [x] 7.5 Add test for map_env_to_config with TRACKER_* variables
- [x] 7.6 Add test for nested key generation (TRACKER_GITHUB_TOKEN → tracker.config.token)
- [x] 7.7 Add test for load_config_from_env with prefix filter
- [x] 7.8 Create tests/test_dotenv_integration.py
- [x] 7.9 Add test for .env file loading with load_dotenv
- [x] 7.10 Add test for configuration priority (context > env > system)
- [x] 7.11 Add test for missing .env file (no error)
- [x] 7.12 Add test for .env.local override behavior
- [x] 7.13 Add test for backward compatibility (context-only config)

## 8. Documentation

- [x] 8.1 Update main README.md with .env configuration section
- [x] 8.2 Add "Quick Start" example using .env file
- [x] 8.3 Update agents/project-tracker-agent/README.md
- [x] 8.4 Add .env configuration examples for tracker types
- [x] 8.5 Document environment variable naming convention
- [x] 8.6 Add troubleshooting section for .env issues
- [x] 8.7 Document configuration priority order
- [x] 8.8 Add migration guide for converting context JSON to .env
- [x] 8.9 Update IMPLEMENTATION.md with .env setup steps

## 9. Create Migration Helper Script

- [x] 9.1 Create scripts/context_to_env.py utility
- [x] 9.2 Add function to parse context JSON
- [x] 9.3 Add function to convert nested dict to UPPER_CASE env vars
- [x] 9.4 Add function to generate .env file from context
- [x] 9.5 Add CLI interface for migration script
- [x] 9.6 Add usage documentation for migration script

## 10. Testing and Validation

> **Note:** Implementation complete. Tasks below require manual execution for validation.

- [ ] 10.1 Run all unit tests and verify pass rate (execute: `pytest agents/project-tracker-agent/tests/`)
- [ ] 10.2 Test with .env file containing tracker config
- [ ] 10.3 Test without .env file (backward compatibility)
- [ ] 10.4 Test with partial .env (mixed with context)
- [ ] 10.5 Test .env.local override behavior
- [ ] 10.6 Test environment variable priority (context > env > system)
- [ ] 10.7 Test with invalid .env syntax
- [ ] 10.8 Test with missing required variables
- [ ] 10.9 Verify .env is ignored by git (execute: `git status`)
- [ ] 10.10 Verify .env.example is tracked by git (execute: `git add .env.example`)
- [ ] 10.11 Test migration script with sample context JSON (execute: `python scripts/context_to_env.py --help`)
- [ ] 10.12 Validate all documentation examples work correctly

# MigIQ Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-13

### Added
- **Tracker-first workflow**: Initial tasks (analysis, planning, backlog) are now created as tracker issues before execution
- **Output attachment**: Task outputs automatically attached to tracker issues with collapsible markdown
- **Autonomous mode**: Fully automated execution that continues on failures (`MODE=autonomous`)
- **GitHub repository auto-detection**: Automatically detects repository from git remote
- **Project .env loading**: Migrations automatically load configuration from `<project-path>/.env`
- **Issue commenting**: `add_comment()` method for both GitHub and Local trackers
- **Graphify offline mode**: Knowledge graph building without API key using `graphify update`
- **Status field updates**: Real GitHub Projects v2 status updates (Backlog → In Progress → Done)
- Configuration priority system: CLI > project .env > agent .env > env > defaults

### Changed
- `/mig-graphify` skill now uses offline `graphify update` command instead of `extract`
- GitHub tracker creates real repository issues (not draft issues) when repository is detected
- Improved error handling with proper logging instead of silent failures
- Enhanced status update confirmations in console output

### Fixed
- **GitHub Projects status updates**: Implemented actual GraphQL field updates (was previously a stub)
- **Tracker interface**: Added missing `add_comment()` and `attach_output()` abstract methods
- **Error handling**: Replaced `except: pass` with proper exception logging

### Documentation
- Added comprehensive .env.example with all configuration options
- Updated skills/migration/SKILL.md with autonomous mode guide
- Updated skills/mig-graphify/SKILL.md with offline mode instructions
- Added RELEASE_NOTES.md with detailed changes and migration guide

[0.1.0]: https://github.com/migrationIQ/mig-agent-mesh/releases/tag/v0.1.0

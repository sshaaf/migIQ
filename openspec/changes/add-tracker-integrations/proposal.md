## Why

The project tracker agent currently manages migration tasks only in a local tasks.md file. Teams need integration with external project management tools (GitHub Projects, GitLab, Jira) to track migration progress alongside their existing workflows, enable team collaboration, and maintain visibility across distributed teams.

## What Changes

- Add configurable tracker integration system allowing users to specify their preferred project tracking platform
- Implement local markdown file tracker (tasks.md) as the default integration
- Implement GitHub Projects integration for teams using GitHub
- Create extensible tracker interface for future GitLab and Jira integrations
- Add configuration options to specify tracker type and credentials in migration context
- Update project tracker agent to sync user stories, tasks, and status with configured tracker

## Capabilities

### New Capabilities

- `tracker-integration-interface`: Defines abstract interface for tracker integrations with methods for creating, updating, and syncing issues/stories
- `local-tracker`: Implements local markdown file-based tracker (tasks.md) with existing functionality
- `github-projects-tracker`: Implements GitHub Projects v2 API integration for issue creation, status updates, and field synchronization
- `tracker-configuration`: Configuration system for specifying tracker type, credentials, and project/board identifiers

### Modified Capabilities

- `project-tracking-harness`: Extend to support multiple tracker backends instead of only tasks.md file

## Impact

- `agents/project-tracker-agent/project_tracker.py` - Add tracker abstraction and integration logic
- Configuration files - Add tracker configuration schema
- `tasks.md` - Remains as default/fallback tracker
- Dependencies - Add GitHub API client library (PyGithub or requests)
- Future extensibility - GitLab and Jira integrations will use the same interface

## ADDED Requirements

### Requirement: Auto-create GitHub Project when project number not specified
The system SHALL automatically create a GitHub Project v2 when TRACKER_GITHUB_PROJECT_NUMBER is not configured.

#### Scenario: Project number omitted triggers auto-creation
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER is not set in configuration
- **THEN** system MUST create a new GitHub Project v2 in the specified organization/user

#### Scenario: Project number specified uses existing project
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER is explicitly set
- **THEN** system MUST NOT create a new project and use the specified project

#### Scenario: Auto-created project has descriptive name
- **WHEN** system auto-creates a project
- **THEN** project name MUST include "Migration Agent" and repository/organization name

### Requirement: Resolve organization or user ID for project creation
The system SHALL resolve GitHub organization or user to internal node ID before creating project.

#### Scenario: Organization ID resolution
- **WHEN** TRACKER_GITHUB_ORGANIZATION is an organization
- **THEN** system MUST query organization node ID via GraphQL

#### Scenario: User ID resolution
- **WHEN** TRACKER_GITHUB_ORGANIZATION is a user login
- **THEN** system MUST query user node ID via GraphQL

#### Scenario: Invalid organization or user
- **WHEN** organization/user does not exist
- **THEN** system MUST raise error with helpful message

### Requirement: Use createProjectV2 GraphQL mutation
The system SHALL use GitHub's createProjectV2 mutation to create projects.

#### Scenario: Create with minimal required fields
- **WHEN** creating project
- **THEN** system MUST provide ownerId and title fields

#### Scenario: Return project number after creation
- **WHEN** project creation succeeds
- **THEN** system MUST extract and return project number from response

### Requirement: Handle project creation failures gracefully
The system SHALL handle project creation errors and fall back to LocalTracker.

#### Scenario: Insufficient permissions
- **WHEN** GitHub token lacks project creation permissions
- **THEN** system MUST log error and fall back to LocalTracker

#### Scenario: API rate limit during creation
- **WHEN** GitHub API returns rate limit error
- **THEN** system MUST wait and retry up to 3 times

#### Scenario: Network error during creation
- **WHEN** network error occurs
- **THEN** system MUST log error and fall back to LocalTracker

### Requirement: Display created project information
The system SHALL inform user of created project details for future configuration.

#### Scenario: Print project number to console
- **WHEN** project is auto-created
- **THEN** system MUST print project number and URL to console

#### Scenario: Suggest saving project number
- **WHEN** project is auto-created
- **THEN** system MUST suggest adding TRACKER_GITHUB_PROJECT_NUMBER to .env

#### Scenario: Provide project URL
- **WHEN** project is auto-created
- **THEN** system MUST provide clickable URL to view project in GitHub

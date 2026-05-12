## ADDED Requirements

### Requirement: Create GitHub Project v2 via GraphQL
The system SHALL support creating new GitHub Projects v2 when project number is not specified.

#### Scenario: Create project with owner ID and title
- **WHEN** _create_project_v2() is called
- **THEN** system MUST execute createProjectV2 mutation with ownerId and title

#### Scenario: Return created project number
- **WHEN** project creation succeeds
- **THEN** system MUST extract project number from response URL

#### Scenario: Handle project creation errors
- **WHEN** createProjectV2 mutation fails
- **THEN** system MUST raise TrackerError with GitHub error details

### Requirement: Resolve owner ID from organization or user
The system SHALL resolve organization or user login to GitHub node ID.

#### Scenario: Get organization ID
- **WHEN** _get_owner_id() called with organization login
- **THEN** system MUST query organization node ID via GraphQL

#### Scenario: Get user ID
- **WHEN** organization query returns null
- **THEN** system MUST try user query with same login

#### Scenario: Owner not found
- **WHEN** both organization and user queries return null
- **THEN** system MUST raise error indicating organization/user not found

### Requirement: Auto-create project on initialization
The system SHALL check for missing project number and auto-create if needed.

#### Scenario: Initialize with project number
- **WHEN** GitHubProjectsTracker initialized with project_number
- **THEN** system MUST use existing project

#### Scenario: Initialize without project number
- **WHEN** GitHubProjectsTracker initialized without project_number
- **THEN** system MUST call _create_project_v2() to create new project

#### Scenario: Cache created project number
- **WHEN** project is auto-created
- **THEN** system MUST store project_number for future use

### Requirement: Delete GitHub Project
The system SHALL support deleting GitHub Projects for cleanup.

#### Scenario: Delete project by ID
- **WHEN** delete_project() called with project node ID
- **THEN** system MUST execute deleteProjectV2 mutation

#### Scenario: Delete returns success
- **WHEN** deletion succeeds
- **THEN** method MUST return True

#### Scenario: Delete handles errors
- **WHEN** deletion fails
- **THEN** system MUST log error and return False

## ADDED Requirements

### Requirement: GitHub tracker creates project items
The system SHALL create GitHub Projects v2 items for user stories using GraphQL API.

#### Scenario: Create draft issue in project
- **WHEN** `create_issue()` is called with story data
- **THEN** system MUST execute addProjectV2DraftIssue mutation with story title and description

#### Scenario: Map story fields to project fields
- **WHEN** creating GitHub project item
- **THEN** system MUST map story priority to project Priority field

#### Scenario: Set story points custom field
- **WHEN** creating GitHub project item
- **THEN** system MUST set Story Points custom field if it exists in project

#### Scenario: Return GitHub item ID
- **WHEN** `create_issue()` succeeds
- **THEN** system MUST return GitHub project item ID

### Requirement: GitHub tracker updates project items
The system SHALL update existing GitHub project items when story status changes.

#### Scenario: Update item status
- **WHEN** `update_issue()` is called with status "In Progress"
- **THEN** system MUST update GitHub project item Status field to "In Progress"

#### Scenario: Update item status to Done
- **WHEN** `update_issue()` is called with status "Done"
- **THEN** system MUST update GitHub project item Status field to "Done"

#### Scenario: Update story points
- **WHEN** `update_issue()` is called with story points change
- **THEN** system MUST update Story Points custom field value

### Requirement: GitHub tracker authenticates with PAT
The system SHALL authenticate GitHub API requests using Personal Access Token.

#### Scenario: Use token from environment variable
- **WHEN** GitHub tracker is initialized with token "$GITHUB_TOKEN"
- **THEN** system MUST read token value from GITHUB_TOKEN environment variable

#### Scenario: Include token in GraphQL requests
- **WHEN** making GraphQL API request
- **THEN** system MUST include "Authorization: Bearer <token>" header

#### Scenario: Handle invalid token
- **WHEN** GitHub API returns 401 Unauthorized
- **THEN** system MUST raise authentication error with message indicating token is invalid

### Requirement: GitHub tracker resolves project configuration
The system SHALL resolve GitHub organization and project number from configuration.

#### Scenario: Query project node ID
- **WHEN** GitHub tracker is initialized with organization and project number
- **THEN** system MUST query GitHub API to resolve project node ID

#### Scenario: Cache project node ID
- **WHEN** project node ID is resolved
- **THEN** system MUST cache it to avoid repeated API calls

#### Scenario: Handle project not found
- **WHEN** organization or project number is invalid
- **THEN** system MUST raise configuration error with helpful message

### Requirement: GitHub tracker handles rate limits
The system SHALL respect GitHub API rate limits and implement retry logic.

#### Scenario: Check rate limit in response
- **WHEN** GraphQL response includes rate limit information
- **THEN** system MUST log remaining rate limit quota

#### Scenario: Implement exponential backoff
- **WHEN** GitHub API returns rate limit error
- **THEN** system MUST wait with exponential backoff (1s, 2s, 4s) before retrying

#### Scenario: Fail after max retries
- **WHEN** rate limit persists after 3 retries
- **THEN** system MUST log error and skip remaining sync operations

### Requirement: GitHub tracker maps story data to GitHub fields
The system SHALL map migration story data to appropriate GitHub project fields.

#### Scenario: Map priority values
- **WHEN** story has priority "P0"
- **THEN** system MUST set GitHub Priority field to "High"

#### Scenario: Map priority P1
- **WHEN** story has priority "P1"
- **THEN** system MUST set GitHub Priority field to "Medium"

#### Scenario: Map priority P2 or P3
- **WHEN** story has priority "P2" or "P3"
- **THEN** system MUST set GitHub Priority field to "Low"

#### Scenario: Map status to GitHub status
- **WHEN** story status is "Backlog"
- **THEN** system MUST set GitHub Status field to "Todo"

#### Scenario: Include acceptance criteria in body
- **WHEN** creating GitHub item
- **THEN** system MUST format acceptance criteria as checkbox list in item body

### Requirement: GitHub tracker provides sync summary
The system SHALL return detailed sync results after operations.

#### Scenario: Return created item details
- **WHEN** `create_issue()` succeeds
- **THEN** system MUST return dict with item_id, url, and status

#### Scenario: Return update confirmation
- **WHEN** `update_issue()` succeeds
- **THEN** system MUST return dict with success status and updated fields

#### Scenario: Return error details
- **WHEN** GitHub API request fails
- **THEN** system MUST return dict with error message and API response details

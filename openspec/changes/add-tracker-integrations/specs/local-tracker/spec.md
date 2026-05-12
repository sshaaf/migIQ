## ADDED Requirements

### Requirement: Local tracker manages tasks.md file
The system SHALL provide a LocalTracker that implements TrackerInterface using tasks.md as storage.

#### Scenario: Create issue in tasks.md
- **WHEN** `create_issue()` is called with story data
- **THEN** system MUST append user story to tasks.md in markdown format

#### Scenario: Update issue status in tasks.md
- **WHEN** `update_issue()` is called with status change
- **THEN** system MUST update the corresponding story's status field in tasks.md

#### Scenario: Get issue from tasks.md
- **WHEN** `get_issue()` is called with story ID
- **THEN** system MUST parse tasks.md and return story details as dictionary

#### Scenario: List issues from tasks.md
- **WHEN** `list_issues()` is called
- **THEN** system MUST parse all user stories from tasks.md and return as list

### Requirement: Local tracker preserves existing tasks.md format
The system SHALL maintain backward compatibility with existing tasks.md format and structure.

#### Scenario: Parse existing story format
- **WHEN** LocalTracker reads tasks.md with existing stories
- **THEN** system MUST correctly parse story ID, title, priority, status, and story points

#### Scenario: Update preserves other fields
- **WHEN** LocalTracker updates a story status
- **THEN** system MUST preserve all other fields including description, acceptance criteria, tasks, and notes

#### Scenario: Maintain markdown structure
- **WHEN** LocalTracker writes to tasks.md
- **THEN** system MUST maintain markdown heading levels and formatting

### Requirement: Local tracker updates timestamps
The system SHALL update relevant timestamps when modifying tasks.

#### Scenario: Update started timestamp
- **WHEN** story status changes to "In Progress"
- **THEN** system MUST set Started timestamp to current ISO 8601 datetime

#### Scenario: Update completed timestamp
- **WHEN** story status changes to "Done"
- **THEN** system MUST set Completed timestamp to current ISO 8601 datetime

### Requirement: Local tracker handles file operations safely
The system SHALL handle file I/O errors gracefully when reading or writing tasks.md.

#### Scenario: Tasks file not found
- **WHEN** tasks.md does not exist
- **THEN** system MUST raise FileNotFoundError with clear message

#### Scenario: Tasks file is empty
- **WHEN** tasks.md exists but is empty
- **THEN** system MUST create initial structure with User Stories section

#### Scenario: Concurrent write protection
- **WHEN** multiple processes attempt to write tasks.md simultaneously
- **THEN** system MUST use file locking to prevent corruption

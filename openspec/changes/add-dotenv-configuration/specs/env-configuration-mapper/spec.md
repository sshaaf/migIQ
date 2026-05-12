## ADDED Requirements

### Requirement: Map flat environment variables to nested config
The system SHALL map flat environment variables to nested configuration dictionary structure.

#### Scenario: Map tracker type
- **WHEN** TRACKER_TYPE environment variable is set
- **THEN** system MUST map to config['tracker']['type']

#### Scenario: Map GitHub tracker config
- **WHEN** TRACKER_GITHUB_* variables are set
- **THEN** system MUST map to config['tracker']['config']['*']

#### Scenario: Preserve data types
- **WHEN** mapping environment variables
- **THEN** system MUST convert strings to appropriate types (int, bool, list)

### Requirement: Use underscore as hierarchy separator
The system SHALL use underscore (_) to denote configuration hierarchy levels.

#### Scenario: Two-level hierarchy
- **WHEN** variable name is PREFIX_KEY
- **THEN** system MUST map to config['prefix']['key']

#### Scenario: Three-level hierarchy
- **WHEN** variable name is PREFIX_SECTION_KEY
- **THEN** system MUST map to config['prefix']['section']['key']

#### Scenario: Preserve case in values
- **WHEN** mapping variable value
- **THEN** system MUST preserve original case of value

### Requirement: Convert environment variable to lowercase keys
The system SHALL convert environment variable names to lowercase for config keys.

#### Scenario: Uppercase variable name
- **WHEN** environment variable is TRACKER_TYPE
- **THEN** config key MUST be 'tracker' and 'type' (lowercase)

#### Scenario: Mixed case variable name
- **WHEN** environment variable is Tracker_Type
- **THEN** config key MUST be 'tracker' and 'type' (lowercase)

### Requirement: Parse integer values
The system SHALL parse numeric strings to integers where appropriate.

#### Scenario: Project number is integer
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER="5"
- **THEN** system MUST convert to integer 5

#### Scenario: Port number is integer
- **WHEN** SERVER_PORT="8080"
- **THEN** system MUST convert to integer 8080

### Requirement: Parse boolean values
The system SHALL parse boolean strings to Python boolean values.

#### Scenario: True values
- **WHEN** variable value is "true", "True", "TRUE", "1", "yes"
- **THEN** system MUST convert to boolean True

#### Scenario: False values
- **WHEN** variable value is "false", "False", "FALSE", "0", "no"
- **THEN** system MUST convert to boolean False

### Requirement: Parse list values
The system SHALL parse comma-separated strings to lists.

#### Scenario: Comma-separated list
- **WHEN** TRACKER_GITHUB_LABELS="bug,migration,automated"
- **THEN** system MUST convert to list ['bug', 'migration', 'automated']

#### Scenario: Empty list
- **WHEN** variable value is empty string
- **THEN** system MUST convert to empty list []

#### Scenario: Single item
- **WHEN** variable value has no commas
- **THEN** system MUST create list with single item

### Requirement: Provide load_config_from_env function
The system SHALL provide a load_config_from_env() function that returns configuration dictionary.

#### Scenario: Call with no arguments
- **WHEN** load_config_from_env() is called
- **THEN** system MUST return config dict from environment variables

#### Scenario: Call with prefix filter
- **WHEN** load_config_from_env(prefix='TRACKER') is called
- **THEN** system MUST return config dict only for TRACKER_* variables

#### Scenario: Return empty dict when no vars
- **WHEN** no matching environment variables exist
- **THEN** system MUST return empty dictionary

## ADDED Requirements

### Requirement: Load .env file using python-dotenv
The system SHALL use python-dotenv library to load environment variables from .env file.

#### Scenario: .env file exists and is loaded
- **WHEN** .env file exists in project root
- **THEN** system MUST call load_dotenv() to load variables into os.environ

#### Scenario: .env file does not exist
- **WHEN** .env file does not exist in project root
- **THEN** system MUST continue without error and use system environment variables

#### Scenario: .env file has invalid syntax
- **WHEN** .env file contains invalid syntax
- **THEN** python-dotenv MUST handle gracefully and load valid entries

### Requirement: Search for .env in project root
The system SHALL search for .env file in the project root directory.

#### Scenario: Load from current working directory
- **WHEN** python process starts
- **THEN** system MUST look for .env in current working directory

#### Scenario: Load from specified path
- **WHEN** .env path is explicitly specified
- **THEN** system MUST load from that path

### Requirement: Override system environment variables
The system SHALL NOT override existing system environment variables by default.

#### Scenario: Variable exists in both system and .env
- **WHEN** environment variable exists in system environment
- **THEN** system MUST keep system value unless override flag is set

#### Scenario: Variable only in .env
- **WHEN** environment variable only exists in .env file
- **THEN** system MUST load value from .env

### Requirement: Support .env file comments
The system SHALL support comments in .env files.

#### Scenario: Lines starting with hash
- **WHEN** .env file contains lines starting with #
- **THEN** system MUST treat them as comments and ignore

#### Scenario: Inline comments
- **WHEN** .env file contains values with inline comments
- **THEN** system MUST parse value correctly excluding comment

### Requirement: Handle quoted values
The system SHALL handle quoted values in .env files.

#### Scenario: Single-quoted values
- **WHEN** .env value is enclosed in single quotes
- **THEN** system MUST remove quotes and use literal value

#### Scenario: Double-quoted values
- **WHEN** .env value is enclosed in double quotes
- **THEN** system MUST remove quotes and interpret escape sequences

#### Scenario: Unquoted values
- **WHEN** .env value is not quoted
- **THEN** system MUST use value as-is

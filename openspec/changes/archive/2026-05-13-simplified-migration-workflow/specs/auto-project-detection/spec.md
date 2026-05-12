# auto-project-detection Specification

## Purpose
Automatically detect and validate the project path from the current working directory, eliminating the need for users to explicitly specify --project-path.

## ADDED Requirements

### Requirement: Detect project root from current directory
The system SHALL automatically identify the project root directory from the current working directory.

#### Scenario: User in project root
- **WHEN** user runs migration command from project root directory
- **THEN** system uses current directory as project path

#### Scenario: User in subdirectory
- **WHEN** user runs migration command from a subdirectory (e.g., src/main/java)
- **THEN** system traverses up to find project root (identified by pom.xml, build.gradle, package.json, etc.)

#### Scenario: Cannot find project root
- **WHEN** no project markers are found in current or parent directories
- **THEN** system uses current directory and warns user

### Requirement: Validate project source code exists
The system SHALL validate that source code exists in the detected project path before initiating migration.

#### Scenario: Valid Java project
- **WHEN** project contains src/ directory with .java files
- **THEN** system validates project and proceeds

#### Scenario: Empty or missing source
- **WHEN** detected project path has no source code
- **THEN** system displays error: "No source code found in {path}. Please run from a project directory or specify --project-path."

#### Scenario: Multiple source directories
- **WHEN** project contains multiple source roots (e.g., multi-module Maven)
- **THEN** system detects all source roots and includes them in project context

### Requirement: Identify project type and build system
The system SHALL identify the project's build system and structure.

#### Scenario: Maven project detection
- **WHEN** pom.xml exists in project root
- **THEN** system identifies project as Maven and extracts metadata (groupId, artifactId, dependencies)

#### Scenario: Gradle project detection
- **WHEN** build.gradle or build.gradle.kts exists
- **THEN** system identifies project as Gradle and extracts configuration

#### Scenario: Unknown build system
- **WHEN** no recognized build file exists
- **THEN** system proceeds with generic Java project detection based on source structure

### Requirement: Provide clear feedback on detected project
The system SHALL display the detected project information to the user before proceeding.

#### Scenario: Confirmation of detected project
- **WHEN** project is auto-detected
- **THEN** system displays: "Detected project: {name} at {path} (Maven/Gradle)"

#### Scenario: User override option
- **WHEN** auto-detected path is incorrect
- **THEN** user can override with --project-path flag

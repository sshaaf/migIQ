#!/usr/bin/env python3
"""
Migration Orchestrator Skill

Main entry point for code migration workflows.
Initializes context and delegates to project-tracker-agent.
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path


class MigrationOrchestrator:
    """Orchestrates the complete migration workflow"""

    SUPPORTED_MIGRATION_TYPES = ["framework", "language", "platform", "custom"]
    SUPPORTED_KANBAN_PLATFORMS = ["jira", "linear", "github-projects"]
    SUPPORTED_CI_PLATFORMS = ["gitlab", "github"]

    def __init__(self, args):
        self.args = args
        self.session_id = f"mig-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
        self.trace_id = f"migration-session-{uuid.uuid4().hex[:8]}"

    def validate_inputs(self):
        """Validate all input parameters"""
        errors = []

        # Validate project path
        if not os.path.exists(self.args.project_path):
            errors.append(f"Project path does not exist: {self.args.project_path}")
        elif not os.path.isdir(self.args.project_path):
            errors.append(f"Project path is not a directory: {self.args.project_path}")

        # Validate migration type
        if self.args.migration_type not in self.SUPPORTED_MIGRATION_TYPES:
            errors.append(
                f"Invalid migration type: {self.args.migration_type}. "
                f"Supported: {', '.join(self.SUPPORTED_MIGRATION_TYPES)}"
            )

        # Validate Kanban platform if provided
        if self.args.kanban_platform and self.args.kanban_platform not in self.SUPPORTED_KANBAN_PLATFORMS:
            errors.append(
                f"Invalid Kanban platform: {self.args.kanban_platform}. "
                f"Supported: {', '.join(self.SUPPORTED_KANBAN_PLATFORMS)}"
            )

        # Validate CI platform if provided
        if self.args.ci_platform and self.args.ci_platform not in self.SUPPORTED_CI_PLATFORMS:
            errors.append(
                f"Invalid CI platform: {self.args.ci_platform}. "
                f"Supported: {', '.join(self.SUPPORTED_CI_PLATFORMS)}"
            )

        if errors:
            return False, errors
        return True, []

    def initialize_context(self):
        """Initialize migration context and configuration files"""

        # Create rule.md if it doesn't exist
        if not os.path.exists(self.args.rules):
            self._create_template_rules()
            print(f"✓ Created template rule file: {self.args.rules}")

        # Create tasks.md if it doesn't exist
        if not os.path.exists(self.args.tasks):
            self._create_initial_tasks()
            print(f"✓ Created initial tasks file: {self.args.tasks}")
        else:
            # Update existing tasks.md with new session
            self._update_tasks_with_session()
            print(f"✓ Updated tasks file with new session: {self.args.tasks}")

        print(f"✓ Migration session initialized: {self.session_id}")
        print(f"✓ Trace ID: {self.trace_id}")

    def _create_template_rules(self):
        """Create a template rule.md file"""
        template = f"""# Migration Rules

## Session: {self.session_id}
**Project**: {self.args.project_path}
**Type**: {self.args.migration_type}

## Transformation Rules

### Code Patterns
- TBD: Define transformation patterns

### Anti-Patterns
- TBD: Define anti-patterns to detect and fix

### Quality Thresholds
- Test coverage: >= 80%
- Code complexity: <= 10 (cyclomatic)
- Security: No critical vulnerabilities

### Architecture Guidelines
- TBD: Define architectural patterns

## Migration Strategy

### Prioritization
- Risk-based: High-risk components first
- Dependency-based: Resolve dependencies first

### Testing Strategy
- Generate characterization tests before refactoring
- Generate functional tests for new behavior
- Validate coverage meets thresholds

## External References
- Migration documentation: TBD
- API documentation: TBD
"""
        with open(self.args.rules, 'w') as f:
            f.write(template)

    def _create_initial_tasks(self):
        """Create initial tasks.md with task structure"""
        # Check if template exists
        template_path = Path(__file__).parent / "tasks.md.template"

        if template_path.exists():
            # Use template
            with open(template_path, 'r') as f:
                template_content = f.read()

            # Add session info at the top
            session_header = f"""# Migration Tasks

## Session: {self.session_id}
**Project**: {self.args.project_path}
**Type**: {self.args.migration_type}
**Started**: {datetime.now().isoformat()}
**Trace ID**: {self.trace_id}

---

## Initial Tasks

### TASK-001: Analyze Codebase
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Outcome**: analysis-report.json
- **Dependencies**: None
- **Started**: -
- **Completed**: -
- **Description**: Analyze target codebase to identify migration requirements, dependencies, and complexity

### TASK-002: Create Migration Plan
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Outcome**: migration-plan.json
- **Dependencies**: TASK-001
- **Started**: -
- **Completed**: -
- **Description**: Generate prioritized user stories and task breakdown from codebase analysis

### TASK-003: Generate Backlog
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Outcome**: tasks.md updated, Kanban synced
- **Dependencies**: TASK-002
- **Started**: -
- **Completed**: -
- **Description**: Create Kanban tickets from migration plan and sync with board

---

"""
            # Combine with template (skip the template header)
            tasks_content = session_header + "\n".join(template_content.split("\n")[3:])
        else:
            # Fallback to simple structure
            tasks_content = f"""# Migration Tasks

## Session: {self.session_id}
**Project**: {self.args.project_path}
**Type**: {self.args.migration_type}
**Started**: {datetime.now().isoformat()}
**Trace ID**: {self.trace_id}

## Initial Tasks

### TASK-001: Analyze Codebase
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Outcome**: analysis-report.json
- **Dependencies**: None
- **Started**: -
- **Completed**: -
- **Description**: Analyze target codebase to identify migration requirements, dependencies, and complexity

### TASK-002: Create Migration Plan
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Outcome**: migration-plan.json
- **Dependencies**: TASK-001
- **Started**: -
- **Completed**: -
- **Description**: Generate prioritized user stories and task breakdown from codebase analysis

### TASK-003: Generate Backlog
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Outcome**: tasks.md updated, Kanban synced
- **Dependencies**: TASK-002
- **Started**: -
- **Completed**: -
- **Description**: Create Kanban tickets from migration plan and sync with board

## User Stories

_User stories will be added here after TASK-003 completes_

## Progress Summary

- **Total Tasks**: 3
- **Pending**: 3
- **In Progress**: 0
- **Completed**: 0
- **Failed**: 0
"""

        with open(self.args.tasks, 'w') as f:
            f.write(tasks_content)

    def _update_tasks_with_session(self):
        """Update existing tasks.md with new session info"""
        # For now, just append new session
        # In production, this would merge intelligently
        with open(self.args.tasks, 'a') as f:
            f.write(f"\n\n---\n\n# New Session: {self.session_id}\n")
            f.write(f"**Started**: {datetime.now().isoformat()}\n")
            f.write(f"**Trace ID**: {self.trace_id}\n\n")

    def invoke_project_tracker(self):
        """Delegate control to project-tracker-agent"""
        context = {
            "sessionId": self.session_id,
            "traceId": self.trace_id,
            "projectPath": os.path.abspath(self.args.project_path),
            "migrationType": self.args.migration_type,
            "rulesPath": os.path.abspath(self.args.rules),
            "tasksPath": os.path.abspath(self.args.tasks),
            "mode": self.args.mode,
        }

        # Add optional configurations
        if self.args.kanban_platform:
            context["kanban"] = {
                "platform": self.args.kanban_platform,
                "project": self.args.kanban_project,
            }

        if self.args.ci_platform:
            context["ci"] = {
                "platform": self.args.ci_platform,
            }

        # Display delegation info
        print("\n" + "="*60)
        print("DELEGATING TO PROJECT-TRACKER-AGENT")
        print("="*60)
        print(f"\nContext:")
        print(json.dumps(context, indent=2))

        # Invoke the project-tracker-agent
        # Find the agent script
        script_dir = Path(__file__).parent.parent.parent
        agent_script = script_dir / "agents" / "project-tracker-agent" / "project_tracker.py"

        if not agent_script.exists():
            print(f"\n⚠ Warning: Agent script not found at {agent_script}")
            print(f"→ Expected invocation:")
            print(f"   python3 {agent_script} --context '{json.dumps(context)}'")
            return context

        # Execute the agent
        print(f"\n→ Invoking: {agent_script}")
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(agent_script), "--context", json.dumps(context)],
                capture_output=False,
                text=True
            )

            if result.returncode != 0:
                print(f"\n✗ Agent execution failed with code {result.returncode}")
            else:
                print(f"\n✓ Agent execution completed successfully")

        except Exception as e:
            print(f"\n✗ Error invoking agent: {e}")
            print(f"→ Manual invocation:")
            print(f"   python3 {agent_script} --context '{json.dumps(context)}'")

        return context

    def generate_response(self, context):
        """Generate success response"""
        response = {
            "sessionId": self.session_id,
            "traceId": self.trace_id,
            "status": "initiated",
            "projectTrackerAgent": "ready_to_run",
            "context": context,
            "tasks": {
                "total": 3,
                "pending": 3,
                "in_progress": 0,
                "completed": 0
            },
            "message": "Migration initialized. Ready to invoke project-tracker-agent.",
            "next_steps": [
                "1. Review generated rule.md and tasks.md files",
                "2. Customize rules if needed",
                "3. Project-tracker-agent will execute the initial tasks",
                "4. Monitor progress in tasks.md and Kanban board"
            ]
        }
        return response

    def run(self):
        """Execute the migration orchestration"""
        print("\n" + "="*60)
        print("MIGRATION ORCHESTRATOR")
        print("="*60)
        print(f"\nProject: {self.args.project_path}")
        print(f"Type: {self.args.migration_type}")
        print(f"Mode: {self.args.mode}")
        print("\nValidating inputs...")

        # Validate inputs
        valid, errors = self.validate_inputs()
        if not valid:
            print("\n✗ Validation failed:")
            for error in errors:
                print(f"  - {error}")
            return {"status": "error", "errors": errors}

        print("✓ All inputs validated")

        # Initialize context
        print("\nInitializing migration context...")
        self.initialize_context()

        # Invoke project tracker
        print("\nPreparing to delegate to project-tracker-agent...")
        context = self.invoke_project_tracker()

        # Generate response
        response = self.generate_response(context)

        print("\n" + "="*60)
        print("MIGRATION RESPONSE")
        print("="*60)
        print(json.dumps(response, indent=2))

        return response


def main():
    parser = argparse.ArgumentParser(
        description="Migration Orchestrator - Main entry point for code migration"
    )

    parser.add_argument(
        "--project-path",
        required=True,
        help="Path to the project to migrate"
    )

    parser.add_argument(
        "--migration-type",
        required=True,
        choices=MigrationOrchestrator.SUPPORTED_MIGRATION_TYPES,
        help="Type of migration"
    )

    parser.add_argument(
        "--rules",
        default="./rule.md",
        help="Path to rule.md file (default: ./rule.md)"
    )

    parser.add_argument(
        "--tasks",
        default="./tasks.md",
        help="Path to tasks.md file (default: ./tasks.md)"
    )

    parser.add_argument(
        "--kanban-platform",
        choices=MigrationOrchestrator.SUPPORTED_KANBAN_PLATFORMS,
        help="Kanban platform (jira, linear, github-projects)"
    )

    parser.add_argument(
        "--kanban-project",
        help="Kanban project/board ID"
    )

    parser.add_argument(
        "--ci-platform",
        choices=MigrationOrchestrator.SUPPORTED_CI_PLATFORMS,
        help="CI platform (gitlab, github)"
    )

    parser.add_argument(
        "--mode",
        choices=["interactive", "autonomous"],
        default="interactive",
        help="Execution mode (default: interactive)"
    )

    args = parser.parse_args()

    orchestrator = MigrationOrchestrator(args)
    result = orchestrator.run()

    # Exit with appropriate code
    sys.exit(0 if result.get("status") != "error" else 1)


if __name__ == "__main__":
    main()

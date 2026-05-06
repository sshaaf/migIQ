#!/usr/bin/env python3
"""
Configuration Validation Utility

Validates rule.md, tasks.md, and CLAUDE.md configuration files
for required structure and content.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple


class ConfigValidator:
    """Validates migration system configuration files"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> bool:
        """Validate all configuration files"""
        print("🔍 Validating configuration files...")
        print()

        rule_md_valid = self.validate_rule_md()
        tasks_md_valid = self.validate_tasks_md()
        claude_md_valid = self.validate_claude_md()

        self._print_results()

        return rule_md_valid and tasks_md_valid and claude_md_valid

    def validate_rule_md(self) -> bool:
        """Validate rule.md structure and content"""
        file_path = self.project_root / "rule.md"

        if not file_path.exists():
            self.errors.append("❌ rule.md not found")
            return False

        content = file_path.read_text()

        # Required sections
        required_sections = [
            "Code Transformation Rules",
            "Quality Thresholds",
            "Testing Requirements",
        ]

        for section in required_sections:
            if section not in content:
                self.errors.append(f"❌ rule.md missing required section: {section}")

        # Check for quality thresholds
        if "Test Coverage" not in content:
            self.warnings.append("⚠️  rule.md missing Test Coverage thresholds")

        if "Code Quality" not in content:
            self.warnings.append("⚠️  rule.md missing Code Quality thresholds")

        if "Performance" not in content:
            self.warnings.append("⚠️  rule.md missing Performance thresholds")

        # Check for at least one transformation rule
        if not re.search(r"#### Rule:", content):
            self.warnings.append("⚠️  rule.md has no transformation rules defined")

        print("✓ rule.md structure validated")
        return len([e for e in self.errors if "rule.md" in e]) == 0

    def validate_tasks_md(self) -> bool:
        """Validate tasks.md structure and content"""
        file_path = self.project_root / "tasks.md"

        if not file_path.exists():
            self.errors.append("❌ tasks.md not found")
            return False

        content = file_path.read_text()

        # Check for markdown task format
        task_pattern = r"- \[([ x])\]"
        tasks = re.findall(task_pattern, content)

        if not tasks:
            self.warnings.append("⚠️  tasks.md has no tasks defined")
        else:
            total_tasks = len(tasks)
            completed_tasks = sum(1 for t in tasks if t == 'x')
            print(f"  Tasks: {completed_tasks}/{total_tasks} complete")

        # Check for story structure (if using story format)
        if "Story:" in content or "User Story" in content:
            required_story_fields = ["Priority:", "Status:", "Description:"]
            for field in required_story_fields:
                if field not in content:
                    self.warnings.append(f"⚠️  tasks.md story template missing: {field}")

        print("✓ tasks.md structure validated")
        return len([e for e in self.errors if "tasks.md" in e]) == 0

    def validate_claude_md(self) -> bool:
        """Validate CLAUDE.md structure and content"""
        file_path = self.project_root / "CLAUDE.md"

        if not file_path.exists():
            self.errors.append("❌ CLAUDE.md not found")
            return False

        content = file_path.read_text()

        # Required sections for Claude Code
        required_sections = [
            "Project Context",
            "Migration Workflow",
        ]

        for section in required_sections:
            if section not in content:
                self.warnings.append(f"⚠️  CLAUDE.md missing recommended section: {section}")

        # Check for quality gates
        if "Quality Gates" not in content and "quality" not in content.lower():
            self.warnings.append("⚠️  CLAUDE.md missing quality gate definitions")

        # Check for testing requirements
        if "Test" not in content and "testing" not in content.lower():
            self.warnings.append("⚠️  CLAUDE.md missing testing requirements")

        print("✓ CLAUDE.md structure validated")
        return len([e for e in self.errors if "CLAUDE.md" in e]) == 0

    def validate_env_config(self) -> bool:
        """Validate .env configuration"""
        env_example = self.project_root / ".env.example"
        env_file = self.project_root / ".env"

        if not env_example.exists():
            self.warnings.append("⚠️  .env.example not found (recommended)")
            return True

        if not env_file.exists():
            self.warnings.append("⚠️  .env not found (copy from .env.example)")
            return True

        # Check for required environment variables
        required_vars = [
            "CI_PLATFORM_TYPE",
            "KANBAN_PLATFORM",
            "OPENCODE_AGENT_API",
        ]

        env_content = env_file.read_text()
        for var in required_vars:
            if var not in env_content or f"{var}=" in env_content and "your-" in env_content:
                self.warnings.append(f"⚠️  Environment variable {var} not configured")

        print("✓ Environment configuration validated")
        return True

    def validate_directory_structure(self) -> bool:
        """Validate required directory structure exists"""
        required_dirs = [
            ".claude/agents",
            ".claude/skills",
            "templates",
            "specs",
            "rules",
            "benchmarks",
            "docs/adr",
        ]

        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                self.errors.append(f"❌ Required directory missing: {dir_path}")

        print("✓ Directory structure validated")
        return len([e for e in self.errors if "directory" in e.lower()]) == 0

    def _print_results(self):
        """Print validation results"""
        print()
        print("=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)

        if self.errors:
            print()
            print("ERRORS:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print()
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.errors and not self.warnings:
            print()
            print("✅ All validation checks passed!")

        print()
        print(f"Summary: {len(self.errors)} errors, {len(self.warnings)} warnings")
        print("=" * 60)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate migration system configuration files"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Path to project root directory (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )

    args = parser.parse_args()

    validator = ConfigValidator(args.project_root)

    # Run all validations
    valid = validator.validate_all()
    validator.validate_env_config()
    validator.validate_directory_structure()

    # Exit code
    if not valid or (args.strict and validator.warnings):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

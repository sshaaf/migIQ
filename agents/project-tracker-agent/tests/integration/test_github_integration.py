#!/usr/bin/env python3
"""
Integration tests for GitHub Projects tracker.

These tests make real API calls to GitHub and require valid credentials
configured in .env.test file.

Usage:
    python -m pytest tests/integration/test_github_integration.py
    python tests/integration/test_github_integration.py  # Run as script
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from trackers.github_tracker import GitHubProjectsTracker
from trackers.config import ConfigurationError
from trackers.interface import TrackerError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntegrationTestError(Exception):
    """Exception raised when integration test fails"""
    pass


def load_test_config() -> Dict:
    """
    Load test configuration from .env.test file.

    Returns:
        Configuration dictionary

    Raises:
        IntegrationTestError: If .env.test is missing or invalid
    """
    env_test_path = Path(__file__).parent.parent.parent / '.env.test'

    if not env_test_path.exists():
        raise IntegrationTestError(
            f".env.test file not found at {env_test_path}\n\n"
            "Please create .env.test from .env.test.example:\n"
            "  cp .env.test.example .env.test\n"
            "  # Edit .env.test and add your GitHub credentials"
        )

    # Load .env.test
    load_dotenv(dotenv_path=env_test_path)

    return {
        'token': os.getenv('TRACKER_GITHUB_TOKEN'),
        'organization': os.getenv('TRACKER_GITHUB_ORGANIZATION'),
        'project_number': os.getenv('TRACKER_GITHUB_PROJECT_NUMBER'),
        'project_name': os.getenv('TRACKER_GITHUB_PROJECT_NAME'),
        'project_description': os.getenv('TRACKER_GITHUB_PROJECT_DESCRIPTION'),
        'keep_project': os.getenv('TEST_KEEP_PROJECT', 'false').lower() == 'true',
        'min_rate_limit': int(os.getenv('TEST_MIN_RATE_LIMIT', '20'))
    }


def validate_test_config(config: Dict) -> None:
    """
    Validate test configuration has required fields.

    Args:
        config: Test configuration dictionary

    Raises:
        IntegrationTestError: If required fields are missing
    """
    required_fields = ['token', 'organization']
    missing_fields = [
        field for field in required_fields
        if not config.get(field)
    ]

    if missing_fields:
        raise IntegrationTestError(
            f"Missing required test configuration fields: {', '.join(missing_fields)}\n\n"
            "Please set these in your .env.test file:\n" +
            "\n".join(f"  TRACKER_GITHUB_{field.upper()}=..." for field in missing_fields)
        )


def check_rate_limit(tracker: GitHubProjectsTracker, min_limit: int = 20) -> Dict:
    """
    Check GitHub API rate limit before starting tests.

    Args:
        tracker: GitHub tracker instance
        min_limit: Minimum rate limit required to run tests

    Returns:
        Rate limit info dictionary

    Raises:
        IntegrationTestError: If rate limit is too low
    """
    query = """
    query {
      rateLimit {
        limit
        cost
        remaining
        resetAt
      }
    }
    """

    try:
        result = tracker._execute_graphql(query, {})
        rate_limit = result.get('data', {}).get('rateLimit', {})

        remaining = rate_limit.get('remaining', 0)
        reset_at = rate_limit.get('resetAt', 'unknown')

        logger.info(f"GitHub API rate limit: {remaining} remaining")

        if remaining < min_limit:
            raise IntegrationTestError(
                f"GitHub API rate limit too low: {remaining} remaining (need {min_limit})\n"
                f"Rate limit resets at: {reset_at}\n"
                "Please wait for rate limit to reset before running integration tests."
            )

        return rate_limit

    except TrackerError as e:
        raise IntegrationTestError(f"Failed to check rate limit: {e}")


def generate_test_project_name(organization: str) -> str:
    """
    Generate unique test project name with timestamp.

    Args:
        organization: Organization name

    Returns:
        Project name string
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"Migration Agent Test - {organization} - {timestamp}"


def print_test_progress(message: str) -> None:
    """
    Print test progress message.

    Args:
        message: Progress message to print
    """
    print(f"\n{'='*70}")
    print(f"  {message}")
    print(f"{'='*70}")


def assert_test(condition: bool, message: str) -> None:
    """
    Custom assertion with helpful error messages.

    Args:
        condition: Condition to check
        message: Error message if condition is False

    Raises:
        IntegrationTestError: If condition is False
    """
    if not condition:
        raise IntegrationTestError(f"Assertion failed: {message}")


def test_create_project(tracker: GitHubProjectsTracker, config: Dict) -> str:
    """
    Test creating a GitHub Project.

    Args:
        tracker: GitHub tracker instance
        config: Test configuration

    Returns:
        Created project number

    Raises:
        IntegrationTestError: If project creation fails
    """
    print_test_progress("TEST: Create GitHub Project")

    try:
        # Get owner ID
        owner_id = tracker._get_owner_id(config['organization'])
        logger.info(f"✓ Resolved owner ID: {owner_id}")

        # Generate project name
        project_name = config.get('project_name') or generate_test_project_name(config['organization'])

        # Create project
        project_number = tracker._create_project_v2(owner_id, project_name)
        logger.info(f"✓ Created project #{project_number}: {project_name}")

        assert_test(
            project_number is not None,
            "Project number should not be None"
        )
        assert_test(
            isinstance(project_number, int),
            f"Project number should be int, got {type(project_number)}"
        )

        print(f"\n✓ Test passed: Created project #{project_number}")
        print(f"  URL: https://github.com/orgs/{config['organization']}/projects/{project_number}")

        return project_number

    except Exception as e:
        raise IntegrationTestError(f"Failed to create project: {e}")


def test_create_items(tracker: GitHubProjectsTracker, project_number: int) -> list:
    """
    Test creating project items.

    Args:
        tracker: GitHub tracker instance
        project_number: Project number to create items in

    Returns:
        List of created item IDs

    Raises:
        IntegrationTestError: If item creation fails
    """
    print_test_progress("TEST: Create Project Items")

    # Update tracker to use the created project
    tracker.project_number = project_number
    tracker._project_node_id = None  # Reset cache

    test_stories = [
        {
            'id': 'TEST-001',
            'title': 'Test Story 1 - High Priority',
            'description': 'Integration test story with high priority',
            'priority': 'P0',
            'status': 'Backlog',
            'acceptance_criteria': [
                'Criterion 1 should pass',
                'Criterion 2 should pass'
            ],
            'affected_modules': ['test-module'],
            'dependencies': ['None'],
            'migration_type': 'test'
        },
        {
            'id': 'TEST-002',
            'title': 'Test Story 2 - Medium Priority',
            'description': 'Integration test story with medium priority',
            'priority': 'P1',
            'status': 'Backlog',
            'acceptance_criteria': ['Test criterion'],
            'affected_modules': ['test-module'],
            'dependencies': ['TEST-001'],
            'migration_type': 'test'
        },
        {
            'id': 'TEST-003',
            'title': 'Test Story 3 - Low Priority',
            'description': 'Integration test story with low priority',
            'priority': 'P2',
            'status': 'Backlog',
            'acceptance_criteria': ['Test criterion'],
            'affected_modules': ['test-module'],
            'dependencies': ['None'],
            'migration_type': 'test'
        }
    ]

    created_items = []

    try:
        for story in test_stories:
            item_id = tracker.create_issue(story)
            created_items.append(item_id)
            logger.info(f"✓ Created item {story['id']}: {item_id}")
            time.sleep(0.5)  # Rate limit protection

        assert_test(
            len(created_items) == 3,
            f"Should create 3 items, created {len(created_items)}"
        )

        print(f"\n✓ Test passed: Created {len(created_items)} items")
        for i, item_id in enumerate(created_items, 1):
            print(f"  Item {i}: {item_id}")

        return created_items

    except Exception as e:
        raise IntegrationTestError(f"Failed to create items: {e}")


def test_verify_items(tracker: GitHubProjectsTracker, item_ids: list) -> None:
    """
    Test verifying created items exist with correct fields.

    Args:
        tracker: GitHub tracker instance
        item_ids: List of item IDs to verify

    Raises:
        IntegrationTestError: If verification fails
    """
    print_test_progress("TEST: Verify Project Items")

    try:
        for item_id in item_ids:
            item = tracker.get_issue(item_id)

            assert_test(
                item is not None,
                f"Item {item_id} should exist"
            )
            assert_test(
                'id' in item,
                f"Item {item_id} should have 'id' field"
            )
            assert_test(
                'title' in item,
                f"Item {item_id} should have 'title' field"
            )

            logger.info(f"✓ Verified item {item_id}: {item.get('title', 'No title')}")
            time.sleep(0.5)  # Rate limit protection

        print(f"\n✓ Test passed: Verified {len(item_ids)} items")

    except Exception as e:
        raise IntegrationTestError(f"Failed to verify items: {e}")


def test_list_items(tracker: GitHubProjectsTracker) -> None:
    """
    Test listing project items.

    Args:
        tracker: GitHub tracker instance

    Raises:
        IntegrationTestError: If listing fails
    """
    print_test_progress("TEST: List Project Items")

    try:
        items = tracker.list_issues()

        assert_test(
            items is not None,
            "list_issues should return a list"
        )
        assert_test(
            len(items) >= 3,
            f"Should have at least 3 items, found {len(items)}"
        )

        logger.info(f"✓ Listed {len(items)} items")
        print(f"\n✓ Test passed: Listed {len(items)} items")

    except Exception as e:
        raise IntegrationTestError(f"Failed to list items: {e}")


def cleanup_project(tracker: GitHubProjectsTracker, keep_project: bool = False) -> None:
    """
    Clean up test project.

    Args:
        tracker: GitHub tracker instance
        keep_project: Whether to keep project after test

    Raises:
        IntegrationTestError: If cleanup fails
    """
    if keep_project:
        print("\n[INFO] Keeping test project (TEST_KEEP_PROJECT=true)")
        return

    print_test_progress("CLEANUP: Delete Test Project")

    try:
        # Get project node ID
        project_id = tracker._resolve_project_node_id()

        # Delete project
        success = tracker.delete_project(project_id)

        if success:
            logger.info("✓ Successfully deleted test project")
            print("\n✓ Cleanup complete: Project deleted")
        else:
            logger.warning("⚠ Failed to delete test project (non-fatal)")
            print("\n⚠ Warning: Failed to delete test project")

    except Exception as e:
        logger.error(f"Cleanup error: {e}")
        print(f"\n⚠ Warning: Cleanup failed: {e}")


def run_integration_tests(json_output: bool = False) -> Dict:
    """
    Run all integration tests.

    Args:
        json_output: Whether to output results in JSON format

    Returns:
        Test results dictionary
    """
    results = {
        'total_tests': 5,
        'passed': 0,
        'failed': 0,
        'errors': [],
        'project_number': None,
        'project_url': None
    }

    tracker = None
    config = None

    try:
        # Load and validate configuration
        if not json_output:
            print_test_progress("Loading Test Configuration")
        config = load_test_config()
        validate_test_config(config)

        # Create tracker instance (without auto-create for testing)
        tracker_config = {
            'token': config['token'],
            'organization': config['organization'],
            'project_number': int(config['project_number']) if config.get('project_number') else None,
            'auto_create': False  # We'll test creation manually
        }

        if tracker_config['project_number']:
            if not json_output:
                print("\n[WARNING] Using existing project number - tests will modify this project!")
                print(f"Project: https://github.com/orgs/{config['organization']}/projects/{tracker_config['project_number']}")
            tracker = GitHubProjectsTracker(tracker_config)
        else:
            # Create tracker without project_number for manual testing
            tracker_config['auto_create'] = True  # Allow auto-create for tracker instance
            tracker_config.pop('project_number', None)

            # Create minimal tracker first
            temp_config = {
                'token': config['token'],
                'organization': config['organization'],
                'project_number': 1,  # Temporary, will be replaced
                'auto_create': False
            }
            tracker = GitHubProjectsTracker(temp_config)

        # Check rate limit
        if not json_output:
            check_rate_limit(tracker, config['min_rate_limit'])

        # Run tests
        project_number = None
        created_items = []

        try:
            # Test 1: Create project (if not using existing)
            if not config.get('project_number'):
                project_number = test_create_project(tracker, config)
                results['project_number'] = project_number
                results['project_url'] = f"https://github.com/orgs/{config['organization']}/projects/{project_number}"
                results['passed'] += 1
            else:
                project_number = int(config['project_number'])
                results['project_number'] = project_number
                results['project_url'] = f"https://github.com/orgs/{config['organization']}/projects/{project_number}"
                if not json_output:
                    print("\n[SKIP] Project creation test (using existing project)")

            # Test 2: Create items
            created_items = test_create_items(tracker, project_number)
            results['passed'] += 1

            # Test 3: Verify items
            test_verify_items(tracker, created_items)
            results['passed'] += 1

            # Test 4: List items
            test_list_items(tracker)
            results['passed'] += 1

            # Test 5: Cleanup (only if we created the project)
            if not config.get('project_number'):
                cleanup_project(tracker, config['keep_project'])
                results['passed'] += 1
            else:
                if not json_output:
                    print("\n[SKIP] Cleanup test (using existing project)")
                results['passed'] += 1

        except IntegrationTestError as e:
            results['failed'] += 1
            results['errors'].append(str(e))
            if not json_output:
                print(f"\n✗ Test failed: {e}")
            raise

    except IntegrationTestError as e:
        results['failed'] += 1
        results['errors'].append(str(e))
        if not json_output:
            print(f"\n✗ Setup failed: {e}")
        return results

    except Exception as e:
        results['failed'] += 1
        results['errors'].append(f"Unexpected error: {e}")
        if not json_output:
            print(f"\n✗ Unexpected error: {e}")
        return results

    finally:
        # Ensure cleanup runs if project was created (and not in existing project mode)
        if tracker and config and not config.get('project_number') and not config.get('keep_project'):
            try:
                if tracker._project_node_id:
                    cleanup_project(tracker, config.get('keep_project', False))
            except Exception as e:
                logger.error(f"Final cleanup failed: {e}")

    return results


def main():
    """Main entry point for running tests as a script"""
    import argparse

    parser = argparse.ArgumentParser(description='Run GitHub integration tests')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    args = parser.parse_args()

    try:
        results = run_integration_tests(json_output=args.json)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("\n" + "="*70)
            print("  TEST SUMMARY")
            print("="*70)
            print(f"Total tests: {results['total_tests']}")
            print(f"Passed: {results['passed']}")
            print(f"Failed: {results['failed']}")

            if results['project_url']:
                print(f"\nProject URL: {results['project_url']}")

            if results['errors']:
                print("\nErrors:")
                for error in results['errors']:
                    print(f"  - {error}")

            print("="*70)

        # Exit with appropriate code
        sys.exit(0 if results['failed'] == 0 else 1)

    except Exception as e:
        if args.json:
            print(json.dumps({'error': str(e)}, indent=2))
        else:
            print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

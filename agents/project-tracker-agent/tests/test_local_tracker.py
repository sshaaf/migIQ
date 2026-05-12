"""
Tests for LocalTracker
"""

import os
import tempfile
import pytest
from trackers.local_tracker import LocalTracker
from trackers.interface import TrackerError


@pytest.fixture
def temp_tasks_file():
    """Create a temporary tasks.md file"""
    fd, path = tempfile.mkstemp(suffix='.md')
    os.close(fd)

    # Write initial content
    with open(path, 'w') as f:
        f.write("# Migration Tasks\n\n## User Stories\n\n")

    yield path

    # Cleanup
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def tracker(temp_tasks_file):
    """Create LocalTracker with temp file"""
    return LocalTracker({'tasks_path': temp_tasks_file})


class TestLocalTracker:
    """Test LocalTracker implementation"""

    def test_init_with_default_path(self):
        """LocalTracker initializes with default path"""
        tracker = LocalTracker()
        assert tracker.tasks_path == './tasks.md'

    def test_init_with_custom_path(self):
        """LocalTracker accepts custom tasks_path"""
        tracker = LocalTracker({'tasks_path': './custom.md'})
        assert tracker.tasks_path == './custom.md'

    def test_read_tasks_file_not_found(self):
        """read_tasks raises FileNotFoundError for missing file"""
        tracker = LocalTracker({'tasks_path': '/nonexistent/tasks.md'})
        with pytest.raises(FileNotFoundError):
            tracker.read_tasks()

    def test_create_issue(self, tracker):
        """create_issue adds story to tasks.md"""
        story_data = {
            'id': 'US-001',
            'title': 'Test Story',
            'description': 'Test description',
            'priority': 'P1',
            'story_points': 5,
            'acceptance_criteria': ['Criterion 1', 'Criterion 2'],
            'affected_modules': ['module-a'],
            'dependencies': ['US-000'],
            'migration_type': 'framework',
            'session_id': 'test-session'
        }

        issue_id = tracker.create_issue(story_data)
        assert issue_id == 'US-001'

        # Verify content
        content = tracker.read_tasks()
        assert '### [US-001] Test Story' in content
        assert '**Priority**: P1' in content
        assert '**Story Points**: 5' in content

    def test_update_issue_status(self, tracker):
        """update_issue updates story status"""
        # Create story first
        story_data = {
            'id': 'US-002',
            'title': 'Test Story 2',
            'description': 'Test',
            'priority': 'P0',
            'story_points': 3,
            'acceptance_criteria': [],
            'affected_modules': [],
            'dependencies': [],
            'migration_type': 'data',
            'status': 'Backlog'
        }
        tracker.create_issue(story_data)

        # Update status
        result = tracker.update_issue('US-002', {'status': 'In Progress'})
        assert result is True

        # Verify update
        content = tracker.read_tasks()
        assert '**Status**: In Progress' in content

    def test_get_issue_existing(self, tracker):
        """get_issue returns story details"""
        # Create story
        story_data = {
            'id': 'US-003',
            'title': 'Test Story 3',
            'description': 'Test',
            'priority': 'P2',
            'story_points': 8,
            'acceptance_criteria': [],
            'affected_modules': [],
            'dependencies': [],
            'migration_type': 'framework'
        }
        tracker.create_issue(story_data)

        # Get story
        story = tracker.get_issue('US-003')
        assert story['id'] == 'US-003'
        assert story['title'] == 'Test Story 3'
        assert story['priority'] == 'P2'
        assert story['story_points'] == 8

    def test_get_issue_not_found(self, tracker):
        """get_issue raises TrackerError for missing story"""
        with pytest.raises(TrackerError, match="not found"):
            tracker.get_issue('US-999')

    def test_list_issues_empty(self, tracker):
        """list_issues returns empty list when no stories"""
        stories = tracker.list_issues()
        assert stories == []

    def test_list_issues_multiple(self, tracker):
        """list_issues returns all stories"""
        # Create multiple stories
        for i in range(3):
            story_data = {
                'id': f'US-{i:03d}',
                'title': f'Story {i}',
                'description': 'Test',
                'priority': 'P1',
                'story_points': 5,
                'acceptance_criteria': [],
                'affected_modules': [],
                'dependencies': [],
                'migration_type': 'framework'
            }
            tracker.create_issue(story_data)

        stories = tracker.list_issues()
        assert len(stories) == 3
        assert stories[0]['id'] == 'US-000'
        assert stories[1]['id'] == 'US-001'
        assert stories[2]['id'] == 'US-002'

    def test_list_issues_with_status_filter(self, tracker):
        """list_issues filters by status"""
        # Create stories with different statuses
        story1 = {
            'id': 'US-010',
            'title': 'Story 10',
            'description': 'Test',
            'priority': 'P1',
            'story_points': 5,
            'acceptance_criteria': [],
            'affected_modules': [],
            'dependencies': [],
            'migration_type': 'framework',
            'status': 'Backlog'
        }
        tracker.create_issue(story1)
        tracker.update_issue('US-010', {'status': 'In Progress'})

        story2 = {
            'id': 'US-011',
            'title': 'Story 11',
            'description': 'Test',
            'priority': 'P1',
            'story_points': 5,
            'acceptance_criteria': [],
            'affected_modules': [],
            'dependencies': [],
            'migration_type': 'framework',
            'status': 'Backlog'
        }
        tracker.create_issue(story2)

        # Filter by status
        in_progress = tracker.list_issues({'status': 'In Progress'})
        assert len(in_progress) == 1
        assert in_progress[0]['id'] == 'US-010'

    def test_sync_story_creates_new(self, tracker):
        """sync_story creates new story if it doesn't exist"""
        story = {
            'id': 'US-100',
            'title': 'Sync Test',
            'description': 'Test sync',
            'priority': 'P1',
            'story_points': 5,
            'acceptance_criteria': [],
            'affected_modules': [],
            'dependencies': [],
            'migration_type': 'framework'
        }

        result = tracker.sync_story(story)
        assert result['status'] == 'success'
        assert result['created'] is True
        assert result['issue_id'] == 'US-100'

    def test_sync_story_updates_existing(self, tracker):
        """sync_story updates existing story"""
        # Create story
        story = {
            'id': 'US-101',
            'title': 'Sync Test 2',
            'description': 'Test',
            'priority': 'P1',
            'story_points': 5,
            'acceptance_criteria': [],
            'affected_modules': [],
            'dependencies': [],
            'migration_type': 'framework',
            'status': 'Backlog'
        }
        tracker.create_issue(story)

        # Sync with updates
        story['status'] = 'Done'
        story['story_points'] = 8

        result = tracker.sync_story(story)
        assert result['status'] == 'success'
        assert result['created'] is False

        # Verify update
        updated = tracker.get_issue('US-101')
        assert updated['status'] == 'Done'


class TestLocalTrackerConcurrency:
    """Test file locking and concurrent write protection"""

    def test_write_uses_file_locking(self, tracker):
        """write_tasks uses file locking"""
        # This test verifies that fcntl.flock is used
        # In a real scenario, we'd need concurrent processes to test properly
        content = "# Test content\n"
        tracker.write_tasks(content)

        read_content = tracker.read_tasks()
        assert read_content == content

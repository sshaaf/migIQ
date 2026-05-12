"""
Tests for TrackerInterface and factory
"""

import pytest
from trackers import create_tracker
from trackers.interface import TrackerInterface, TrackerError
from trackers.local_tracker import LocalTracker
from trackers.github_tracker import GitHubProjectsTracker


class TestTrackerInterface:
    """Test TrackerInterface abstract methods"""

    def test_interface_is_abstract(self):
        """TrackerInterface cannot be instantiated directly"""
        with pytest.raises(TypeError):
            TrackerInterface()

    def test_interface_defines_required_methods(self):
        """TrackerInterface defines all required methods"""
        required_methods = [
            'create_issue',
            'update_issue',
            'get_issue',
            'list_issues',
            'sync_story'
        ]

        for method in required_methods:
            assert hasattr(TrackerInterface, method)
            assert callable(getattr(TrackerInterface, method))


class TestTrackerFactory:
    """Test create_tracker factory method"""

    def test_factory_defaults_to_local_tracker(self):
        """Factory returns LocalTracker when no config provided"""
        tracker = create_tracker()
        assert isinstance(tracker, LocalTracker)

    def test_factory_creates_local_tracker(self):
        """Factory creates LocalTracker for type 'local'"""
        config = {'type': 'local'}
        tracker = create_tracker(config)
        assert isinstance(tracker, LocalTracker)

    def test_factory_creates_local_with_config(self):
        """Factory passes config to LocalTracker"""
        config = {
            'type': 'local',
            'config': {'tasks_path': './custom-tasks.md'}
        }
        tracker = create_tracker(config)
        assert isinstance(tracker, LocalTracker)
        assert tracker.tasks_path == './custom-tasks.md'

    def test_factory_fallback_for_unsupported_type(self):
        """Factory falls back to LocalTracker for unsupported types"""
        config = {'type': 'gitlab'}
        tracker = create_tracker(config)
        assert isinstance(tracker, LocalTracker)

    def test_factory_fallback_for_unknown_type(self):
        """Factory falls back to LocalTracker for unknown types"""
        config = {'type': 'unknown'}
        tracker = create_tracker(config)
        assert isinstance(tracker, LocalTracker)

    def test_factory_creates_github_tracker(self):
        """Factory creates GitHubProjectsTracker for type 'github'"""
        config = {
            'type': 'github',
            'config': {
                'token': 'fake-token',
                'organization': 'test-org',
                'project_number': 1
            }
        }
        tracker = create_tracker(config)
        assert isinstance(tracker, GitHubProjectsTracker)


class TestTrackerError:
    """Test TrackerError exception"""

    def test_tracker_error_is_exception(self):
        """TrackerError is an Exception"""
        assert issubclass(TrackerError, Exception)

    def test_tracker_error_message(self):
        """TrackerError can be raised with message"""
        with pytest.raises(TrackerError, match="Test error"):
            raise TrackerError("Test error")

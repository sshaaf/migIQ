"""
Tests for GitHubProjectsTracker
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from trackers.github_tracker import GitHubProjectsTracker
from trackers.config import ConfigurationError
from trackers.interface import TrackerError


@pytest.fixture
def github_config():
    """Sample GitHub configuration"""
    return {
        'token': 'test-token',
        'organization': 'test-org',
        'project_number': 1
    }


@pytest.fixture
def tracker(github_config):
    """Create GitHubProjectsTracker with test config"""
    return GitHubProjectsTracker(github_config)


class TestGitHubTrackerInit:
    """Test GitHubProjectsTracker initialization"""

    def test_init_with_valid_config(self, github_config):
        """GitHubProjectsTracker initializes with valid config"""
        tracker = GitHubProjectsTracker(github_config)
        assert tracker.token == 'test-token'
        assert tracker.organization == 'test-org'
        assert tracker.project_number == 1

    def test_init_missing_token(self):
        """Raises ConfigurationError if token missing"""
        config = {'organization': 'test-org', 'project_number': 1}
        with pytest.raises(ConfigurationError, match="token is required"):
            GitHubProjectsTracker(config)

    def test_init_missing_organization(self):
        """Raises ConfigurationError if organization missing"""
        config = {'token': 'test-token', 'project_number': 1}
        with pytest.raises(ConfigurationError, match="organization is required"):
            GitHubProjectsTracker(config)

    @patch.object(GitHubProjectsTracker, '_get_owner_id')
    @patch.object(GitHubProjectsTracker, '_create_project_v2')
    def test_init_auto_create_project(self, mock_create, mock_get_owner, capsys):
        """Auto-creates project when project_number not specified"""
        mock_get_owner.return_value = 'owner-123'
        mock_create.return_value = 5

        config = {'token': 'test-token', 'organization': 'test-org', 'auto_create': True}
        tracker = GitHubProjectsTracker(config)

        assert tracker.project_number == 5
        mock_get_owner.assert_called_once_with('test-org')
        mock_create.assert_called_once()

        # Check console output
        captured = capsys.readouterr()
        assert "Created GitHub Project #5" in captured.out

    def test_init_missing_project_number_auto_create_disabled(self):
        """Raises ConfigurationError if project_number missing and auto_create disabled"""
        config = {'token': 'test-token', 'organization': 'test-org', 'auto_create': False}
        with pytest.raises(ConfigurationError, match="project_number is required"):
            GitHubProjectsTracker(config)

    def test_init_with_project_number_no_auto_create(self):
        """Uses provided project_number without auto-creation"""
        config = {'token': 'test-token', 'organization': 'test-org', 'project_number': 10}
        tracker = GitHubProjectsTracker(config)
        assert tracker.project_number == 10


class TestGitHubTrackerMapping:
    """Test priority and status mapping"""

    def test_map_priority_p0(self, tracker):
        """Maps P0 to High"""
        assert tracker._map_priority('P0') == 'High'

    def test_map_priority_p1(self, tracker):
        """Maps P1 to Medium"""
        assert tracker._map_priority('P1') == 'Medium'

    def test_map_priority_p2_p3(self, tracker):
        """Maps P2/P3 to Low"""
        assert tracker._map_priority('P2') == 'Low'
        assert tracker._map_priority('P3') == 'Low'

    def test_map_priority_unknown(self, tracker):
        """Defaults to Medium for unknown priority"""
        assert tracker._map_priority('PX') == 'Medium'

    def test_map_status_backlog(self, tracker):
        """Maps Backlog to Todo"""
        assert tracker._map_status('Backlog') == 'Todo'

    def test_map_status_in_progress(self, tracker):
        """Maps In Progress to In Progress"""
        assert tracker._map_status('In Progress') == 'In Progress'

    def test_map_status_done(self, tracker):
        """Maps Done to Done"""
        assert tracker._map_status('Done') == 'Done'

    def test_map_status_failed(self, tracker):
        """Maps Failed to Done"""
        assert tracker._map_status('Failed') == 'Done'


class TestGitHubTrackerGraphQL:
    """Test GraphQL execution"""

    @patch('trackers.github_tracker.requests.post')
    def test_execute_graphql_success(self, mock_post, tracker):
        """_execute_graphql executes successful request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {'test': 'result'}
        }
        mock_post.return_value = mock_response

        result = tracker._execute_graphql("query { test }", {})
        assert result['data']['test'] == 'result'

    @patch('trackers.github_tracker.requests.post')
    def test_execute_graphql_401_error(self, mock_post, tracker):
        """_execute_graphql raises TrackerError on 401"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with pytest.raises(TrackerError, match="authentication failed"):
            tracker._execute_graphql("query { test }", {})

    @patch('trackers.github_tracker.requests.post')
    def test_execute_graphql_rate_limit(self, mock_post, tracker):
        """_execute_graphql handles rate limiting"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "rate limit exceeded"
        mock_post.return_value = mock_response

        with pytest.raises(TrackerError, match="rate limit exceeded"):
            tracker._execute_graphql("query { test }", {})

    @patch('trackers.github_tracker.requests.post')
    def test_execute_graphql_network_error(self, mock_post, tracker):
        """_execute_graphql handles network errors"""
        mock_post.side_effect = Exception("Network error")

        with pytest.raises(TrackerError, match="Network error"):
            tracker._execute_graphql("query { test }", {})

    @patch('trackers.github_tracker.requests.post')
    def test_execute_graphql_graphql_errors(self, mock_post, tracker):
        """_execute_graphql handles GraphQL errors"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'errors': [{'message': 'GraphQL error'}]
        }
        mock_post.return_value = mock_response

        with pytest.raises(TrackerError, match="GraphQL error"):
            tracker._execute_graphql("query { test }", {})


class TestGitHubTrackerProjectResolution:
    """Test project node ID resolution"""

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_resolve_project_node_id(self, mock_graphql, tracker):
        """_resolve_project_node_id queries and caches project ID"""
        mock_graphql.return_value = {
            'data': {
                'organization': {
                    'projectV2': {
                        'id': 'project-123',
                        'title': 'Test Project'
                    }
                }
            }
        }

        project_id = tracker._resolve_project_node_id()
        assert project_id == 'project-123'
        assert tracker._project_node_id == 'project-123'

        # Second call should use cache
        project_id_2 = tracker._resolve_project_node_id()
        assert project_id_2 == 'project-123'
        assert mock_graphql.call_count == 1  # Only called once

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_resolve_project_not_found(self, mock_graphql, tracker):
        """_resolve_project_node_id raises TrackerError if project not found"""
        mock_graphql.return_value = {
            'data': {
                'organization': {}
            }
        }

        with pytest.raises(TrackerError, match="project not found"):
            tracker._resolve_project_node_id()


class TestGitHubTrackerCreateIssue:
    """Test issue creation"""

    @patch.object(GitHubProjectsTracker, '_resolve_project_node_id')
    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_create_issue_success(self, mock_graphql, mock_resolve, tracker):
        """create_issue creates draft issue"""
        mock_resolve.return_value = 'project-123'
        mock_graphql.return_value = {
            'data': {
                'addProjectV2DraftIssue': {
                    'projectItem': {
                        'id': 'item-456',
                        'content': {'title': 'Test Story'}
                    }
                }
            }
        }

        story_data = {
            'id': 'US-001',
            'title': 'Test Story',
            'description': 'Test description',
            'acceptance_criteria': ['Criterion 1'],
            'affected_modules': ['module-a'],
            'dependencies': ['US-000'],
            'migration_type': 'framework'
        }

        item_id = tracker.create_issue(story_data)
        assert item_id == 'item-456'


class TestGitHubTrackerRetryLogic:
    """Test retry and exponential backoff"""

    @patch('trackers.github_tracker.requests.post')
    @patch('trackers.github_tracker.time.sleep')
    def test_retry_on_network_error(self, mock_sleep, mock_post, tracker):
        """Retries on network errors with exponential backoff"""
        # Fail twice, succeed on third attempt
        mock_post.side_effect = [
            Exception("Network error 1"),
            Exception("Network error 2"),
            Mock(status_code=200, json=lambda: {'data': {'success': True}})
        ]

        result = tracker._execute_graphql("query { test }", {})
        assert result['data']['success'] is True
        assert mock_sleep.call_count == 2  # Slept between retries
        assert mock_post.call_count == 3


class TestGitHubTrackerOwnerResolution:
    """Test owner ID resolution"""

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_get_owner_id_organization(self, mock_graphql, tracker):
        """_get_owner_id resolves organization to node ID"""
        mock_graphql.return_value = {
            'data': {
                'organization': {
                    'id': 'org-123'
                }
            }
        }

        owner_id = tracker._get_owner_id('test-org')
        assert owner_id == 'org-123'

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_get_owner_id_user_fallback(self, mock_graphql, tracker):
        """_get_owner_id falls back to user query if org not found"""
        # First call returns null org, second call returns user
        mock_graphql.side_effect = [
            {'data': {'organization': None}},
            {'data': {'user': {'id': 'user-456'}}}
        ]

        owner_id = tracker._get_owner_id('test-user')
        assert owner_id == 'user-456'
        assert mock_graphql.call_count == 2

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_get_owner_id_not_found(self, mock_graphql, tracker):
        """_get_owner_id raises error if neither org nor user found"""
        mock_graphql.side_effect = [
            {'data': {'organization': None}},
            {'data': {'user': None}}
        ]

        with pytest.raises(TrackerError, match="not found"):
            tracker._get_owner_id('nonexistent')


class TestGitHubTrackerProjectCreation:
    """Test project creation"""

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_create_project_v2_success(self, mock_graphql, tracker):
        """_create_project_v2 creates project and returns number"""
        mock_graphql.return_value = {
            'data': {
                'createProjectV2': {
                    'projectV2': {
                        'id': 'project-789',
                        'number': 5,
                        'url': 'https://github.com/orgs/test-org/projects/5',
                        'title': 'Test Project'
                    }
                }
            }
        }

        project_number = tracker._create_project_v2('owner-123', 'Test Project')
        assert project_number == 5

        # Verify mutation was called with correct variables
        call_args = mock_graphql.call_args
        assert call_args[0][1]['ownerId'] == 'owner-123'
        assert call_args[0][1]['title'] == 'Test Project'

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_create_project_v2_failure(self, mock_graphql, tracker):
        """_create_project_v2 raises error on failure"""
        mock_graphql.return_value = {
            'data': {
                'createProjectV2': None
            }
        }

        with pytest.raises(TrackerError, match="Failed to create GitHub project"):
            tracker._create_project_v2('owner-123', 'Test Project')

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_create_project_v2_no_number(self, mock_graphql, tracker):
        """_create_project_v2 raises error if number missing in response"""
        mock_graphql.return_value = {
            'data': {
                'createProjectV2': {
                    'projectV2': {
                        'id': 'project-789',
                        'url': 'https://github.com/orgs/test-org/projects/5',
                        'title': 'Test Project'
                        # Missing 'number' field
                    }
                }
            }
        }

        with pytest.raises(TrackerError, match="Failed to extract project number"):
            tracker._create_project_v2('owner-123', 'Test Project')


class TestGitHubTrackerProjectDeletion:
    """Test project deletion"""

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_delete_project_success(self, mock_graphql, tracker):
        """delete_project successfully deletes project"""
        mock_graphql.return_value = {
            'data': {
                'deleteProjectV2': {
                    'projectV2': {
                        'id': 'project-123'
                    }
                }
            }
        }

        result = tracker.delete_project('project-123')
        assert result is True

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_delete_project_failure(self, mock_graphql, tracker):
        """delete_project returns False on failure"""
        mock_graphql.return_value = {
            'data': {
                'deleteProjectV2': None
            }
        }

        result = tracker.delete_project('project-123')
        assert result is False

    @patch.object(GitHubProjectsTracker, '_execute_graphql')
    def test_delete_project_error(self, mock_graphql, tracker):
        """delete_project returns False on exception"""
        mock_graphql.side_effect = TrackerError("GraphQL error")

        result = tracker.delete_project('project-123')
        assert result is False

"""
Tests for configuration validation and environment variable resolution
"""

import os
import pytest
from trackers.config import (
    resolve_env_var,
    validate_tracker_config,
    resolve_config_env_vars,
    ConfigurationError
)


class TestResolveEnvVar:
    """Test environment variable resolution"""

    def test_resolve_normal_string(self):
        """Returns normal string unchanged"""
        assert resolve_env_var("normal_value") == "normal_value"

    def test_resolve_env_var_exists(self, monkeypatch):
        """Resolves $VAR to environment variable value"""
        monkeypatch.setenv("TEST_VAR", "test_value")
        assert resolve_env_var("$TEST_VAR") == "test_value"

    def test_resolve_env_var_missing(self):
        """Raises ConfigurationError if env var doesn't exist"""
        with pytest.raises(ConfigurationError, match="MISSING_VAR"):
            resolve_env_var("$MISSING_VAR")

    def test_resolve_escaped_dollar(self):
        """Resolves $$LITERAL to $LITERAL"""
        assert resolve_env_var("$$LITERAL") == "$LITERAL"

    def test_resolve_non_string(self):
        """Returns non-string values unchanged"""
        assert resolve_env_var(123) == 123
        assert resolve_env_var(None) is None


class TestValidateTrackerConfig:
    """Test tracker configuration validation"""

    def test_validate_local_config_minimal(self):
        """Local config with minimal fields is valid"""
        config = {'type': 'local'}
        assert validate_tracker_config(config) is True

    def test_validate_local_config_with_path(self):
        """Local config with tasks_path is valid"""
        config = {
            'type': 'local',
            'config': {'tasks_path': './custom.md'}
        }
        assert validate_tracker_config(config) is True

    def test_validate_local_config_invalid_path_type(self):
        """Raises error if tasks_path is not string"""
        config = {
            'type': 'local',
            'config': {'tasks_path': 123}
        }
        with pytest.raises(ConfigurationError, match="tasks_path must be a string"):
            validate_tracker_config(config)

    def test_validate_github_config_valid(self):
        """GitHub config with all required fields is valid"""
        config = {
            'type': 'github',
            'config': {
                'token': 'test-token',
                'organization': 'test-org',
                'project_number': 1
            }
        }
        assert validate_tracker_config(config) is True

    def test_validate_github_config_missing_token(self):
        """Raises error if GitHub token is missing"""
        config = {
            'type': 'github',
            'config': {
                'organization': 'test-org',
                'project_number': 1
            }
        }
        with pytest.raises(ConfigurationError, match="missing required fields"):
            validate_tracker_config(config)

    def test_validate_github_config_missing_organization(self):
        """Raises error if GitHub organization is missing"""
        config = {
            'type': 'github',
            'config': {
                'token': 'test-token',
                'project_number': 1
            }
        }
        with pytest.raises(ConfigurationError, match="missing required fields"):
            validate_tracker_config(config)

    def test_validate_github_config_missing_project_number(self):
        """GitHub config without project_number is valid (auto-create)"""
        config = {
            'type': 'github',
            'config': {
                'token': 'test-token',
                'organization': 'test-org'
            }
        }
        # Should not raise - project_number is optional
        assert validate_tracker_config(config) is True

    def test_validate_github_config_with_labels(self):
        """GitHub config with optional labels is valid"""
        config = {
            'type': 'github',
            'config': {
                'token': 'test-token',
                'organization': 'test-org',
                'project_number': 1,
                'labels': ['bug', 'migration']
            }
        }
        assert validate_tracker_config(config) is True

    def test_validate_github_config_invalid_labels_type(self):
        """Raises error if labels is not a list"""
        config = {
            'type': 'github',
            'config': {
                'token': 'test-token',
                'organization': 'test-org',
                'project_number': 1,
                'labels': 'not-a-list'
            }
        }
        with pytest.raises(ConfigurationError, match="labels must be a list"):
            validate_tracker_config(config)

    def test_validate_not_dict(self):
        """Raises error if config is not a dict"""
        with pytest.raises(ConfigurationError, match="must be a dictionary"):
            validate_tracker_config("not a dict")

    def test_validate_unsupported_type(self):
        """Returns True for unsupported types (with warning)"""
        config = {'type': 'jira'}
        # Should not raise, just log warning
        assert validate_tracker_config(config) is True


class TestResolveConfigEnvVars:
    """Test recursive environment variable resolution"""

    def test_resolve_config_simple(self, monkeypatch):
        """Resolves env vars in simple config"""
        monkeypatch.setenv("TEST_TOKEN", "secret-token")

        config = {
            'token': '$TEST_TOKEN',
            'org': 'test-org'
        }

        resolved = resolve_config_env_vars(config)
        assert resolved['token'] == 'secret-token'
        assert resolved['org'] == 'test-org'

    def test_resolve_config_nested(self, monkeypatch):
        """Resolves env vars in nested config"""
        monkeypatch.setenv("GITHUB_TOKEN", "gh-token")

        config = {
            'type': 'github',
            'config': {
                'token': '$GITHUB_TOKEN',
                'organization': 'my-org'
            }
        }

        resolved = resolve_config_env_vars(config)
        assert resolved['config']['token'] == 'gh-token'

    def test_resolve_config_list(self, monkeypatch):
        """Resolves env vars in list values"""
        monkeypatch.setenv("LABEL", "migration")

        config = {
            'labels': ['$LABEL', 'bug']
        }

        resolved = resolve_config_env_vars(config)
        assert resolved['labels'] == ['migration', 'bug']

    def test_resolve_config_non_dict(self):
        """Returns non-dict values unchanged"""
        assert resolve_config_env_vars("string") == "string"
        assert resolve_config_env_vars(123) == 123

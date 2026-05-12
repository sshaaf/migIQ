"""
Tests for dotenv integration and configuration loading
"""

import os
import tempfile
import pytest
from pathlib import Path
from dotenv import load_dotenv
from trackers.config import (
    load_tracker_config_from_env,
    merge_configs
)


@pytest.fixture
def temp_env_file():
    """Create temporary .env file"""
    fd, path = tempfile.mkstemp(suffix='.env')
    yield path
    os.close(fd)
    if os.path.exists(path):
        os.remove(path)


class TestDotenvLoading:
    """Test .env file loading"""

    def test_load_dotenv_file(self, temp_env_file, monkeypatch):
        """Load variables from .env file"""
        # Write .env file
        with open(temp_env_file, 'w') as f:
            f.write('TEST_VAR=test_value\n')
            f.write('TRACKER_TYPE=github\n')

        # Load it
        load_dotenv(temp_env_file)

        # Verify loaded
        assert os.environ.get('TEST_VAR') == 'test_value'
        assert os.environ.get('TRACKER_TYPE') == 'github'

    def test_missing_env_file(self):
        """No error when .env file missing"""
        # Should not raise error
        load_dotenv('/nonexistent/.env')

    def test_env_file_with_comments(self, temp_env_file):
        """Handle comments in .env file"""
        with open(temp_env_file, 'w') as f:
            f.write('# This is a comment\n')
            f.write('VAR1=value1\n')
            f.write('VAR2=value2  # Inline comment\n')

        load_dotenv(temp_env_file)

        assert os.environ.get('VAR1') == 'value1'
        assert os.environ.get('VAR2') == 'value2'


class TestConfigurationPriority:
    """Test configuration priority (context > env > system)"""

    def test_context_overrides_env(self):
        """Context configuration has highest priority"""
        env_config = {'type': 'local'}
        context_config = {'type': 'github'}

        result = merge_configs(env_config, context_config)
        assert result == context_config

    def test_env_used_when_no_context(self):
        """Environment configuration used when no context"""
        env_config = {'type': 'github'}
        context_config = None

        result = merge_configs(env_config, context_config)
        assert result == env_config

    def test_none_when_neither(self):
        """Return None when no configuration from either source"""
        result = merge_configs(None, None)
        assert result is None

    def test_explicit_none_context(self):
        """Context explicitly None uses env config"""
        env_config = {'type': 'local'}
        result = merge_configs(env_config, None)
        assert result == env_config


class TestDotenvLocalOverride:
    """Test .env.local override behavior"""

    def test_env_local_overrides(self):
        """".env.local overrides .env"""
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f1:
            f1.write('VAR1=from_env\n')
            f1.write('VAR2=only_in_env\n')
            env_file = f1.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.env.local', delete=False) as f2:
            f2.write('VAR1=from_local\n')
            local_file = f2.name

        try:
            # Load both
            load_dotenv(env_file)
            load_dotenv(local_file, override=True)

            # VAR1 should be overridden
            assert os.environ.get('VAR1') == 'from_local'
            # VAR2 should still exist
            assert os.environ.get('VAR2') == 'only_in_env'

        finally:
            os.unlink(env_file)
            os.unlink(local_file)


class TestBackwardCompatibility:
    """Test backward compatibility with context-only configuration"""

    def test_context_only_config_works(self):
        """Configuration works with only context, no .env"""
        # No environment variables set
        env_config = None
        context_config = {
            'type': 'github',
            'config': {
                'token': 'test-token',
                'organization': 'test-org',
                'project_number': 1
            }
        }

        result = merge_configs(env_config, context_config)
        assert result == context_config

    def test_existing_scripts_unchanged(self):
        """Existing invocation patterns continue to work"""
        # Simulates existing script passing context JSON
        context = {
            'tracker': {
                'type': 'local',
                'config': {'tasks_path': './tasks.md'}
            }
        }

        # Should work without any environment setup
        result = merge_configs(None, context['tracker'])
        assert result['type'] == 'local'

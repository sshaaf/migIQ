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

        try:
            # Load it
            load_dotenv(temp_env_file)

            # Verify loaded
            assert os.environ.get('TEST_VAR') == 'test_value'
            assert os.environ.get('TRACKER_TYPE') == 'github'
        finally:
            # Cleanup
            os.environ.pop('TEST_VAR', None)
            os.environ.pop('TRACKER_TYPE', None)

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

        try:
            load_dotenv(temp_env_file)

            assert os.environ.get('VAR1') == 'value1'
            assert os.environ.get('VAR2') == 'value2'
        finally:
            # Cleanup
            os.environ.pop('VAR1', None)
            os.environ.pop('VAR2', None)


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
        # Save current environment state
        original_var1 = os.environ.get('VAR1')
        original_var2 = os.environ.get('VAR2')

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
            # Clean up environment variables
            if original_var1 is None:
                os.environ.pop('VAR1', None)
            else:
                os.environ['VAR1'] = original_var1

            if original_var2 is None:
                os.environ.pop('VAR2', None)
            else:
                os.environ['VAR2'] = original_var2

            os.unlink(env_file)
            os.unlink(local_file)


class TestProjectDotenvLoading:
    """Test loading .env from project directory"""

    def test_load_project_env(self):
        """Load .env from project directory"""
        # Create temporary project directory
        with tempfile.TemporaryDirectory() as project_dir:
            # Create .env in project
            env_path = os.path.join(project_dir, '.env')
            with open(env_path, 'w') as f:
                f.write('PROJECT_VAR=project_value\n')
                f.write('TRACKER_GITHUB_TOKEN=ghp_project_token\n')

            # Save current environment
            original_project_var = os.environ.get('PROJECT_VAR')
            original_token = os.environ.get('TRACKER_GITHUB_TOKEN')

            try:
                # Load project .env
                load_dotenv(env_path, override=True)

                # Verify loaded
                assert os.environ.get('PROJECT_VAR') == 'project_value'
                assert os.environ.get('TRACKER_GITHUB_TOKEN') == 'ghp_project_token'
            finally:
                # Cleanup
                if original_project_var is None:
                    os.environ.pop('PROJECT_VAR', None)
                else:
                    os.environ['PROJECT_VAR'] = original_project_var

                if original_token is None:
                    os.environ.pop('TRACKER_GITHUB_TOKEN', None)
                else:
                    os.environ['TRACKER_GITHUB_TOKEN'] = original_token

    def test_project_env_overrides_global(self):
        """Project .env overrides global .env"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create global .env
            global_env = os.path.join(temp_dir, 'global.env')
            with open(global_env, 'w') as f:
                f.write('TRACKER_TYPE=local\n')

            # Create project .env
            project_env = os.path.join(temp_dir, 'project.env')
            with open(project_env, 'w') as f:
                f.write('TRACKER_TYPE=github\n')

            original_tracker_type = os.environ.get('TRACKER_TYPE')

            try:
                # Load global first
                load_dotenv(global_env)
                assert os.environ.get('TRACKER_TYPE') == 'local'

                # Load project with override
                load_dotenv(project_env, override=True)
                assert os.environ.get('TRACKER_TYPE') == 'github'
            finally:
                if original_tracker_type is None:
                    os.environ.pop('TRACKER_TYPE', None)
                else:
                    os.environ['TRACKER_TYPE'] = original_tracker_type


class TestModeConfiguration:
    """Test MODE environment variable loading"""

    def test_mode_from_environment(self):
        """Load MODE from environment variable"""
        original_mode = os.environ.get('MODE')

        try:
            # Set MODE in environment
            os.environ['MODE'] = 'autonomous'

            # Simulate context loading (like project_tracker.py does)
            context = {'mode': None}  # No mode in context
            mode = context.get('mode') or os.environ.get('MODE', 'interactive')

            assert mode == 'autonomous'
        finally:
            if original_mode is None:
                os.environ.pop('MODE', None)
            else:
                os.environ['MODE'] = original_mode

    def test_mode_defaults_to_interactive(self):
        """Default to interactive when MODE not set"""
        original_mode = os.environ.get('MODE')

        try:
            # Remove MODE from environment
            os.environ.pop('MODE', None)

            # Simulate context loading
            context = {'mode': None}
            mode = context.get('mode') or os.environ.get('MODE', 'interactive')

            assert mode == 'interactive'
        finally:
            if original_mode is not None:
                os.environ['MODE'] = original_mode

    def test_context_mode_overrides_env(self):
        """Context mode takes priority over environment"""
        original_mode = os.environ.get('MODE')

        try:
            # Set MODE in environment
            os.environ['MODE'] = 'autonomous'

            # But context has interactive
            context = {'mode': 'interactive'}
            mode = context.get('mode') or os.environ.get('MODE', 'interactive')

            assert mode == 'interactive'
        finally:
            if original_mode is None:
                os.environ.pop('MODE', None)
            else:
                os.environ['MODE'] = original_mode


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

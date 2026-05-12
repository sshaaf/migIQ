"""
Tests for environment variable mapper
"""

import pytest
from trackers.env_mapper import (
    parse_bool,
    parse_int,
    parse_list,
    map_env_to_config,
    load_config_from_env
)


class TestParseBool:
    """Test boolean parsing"""

    def test_parse_true_values(self):
        """Parse various true values"""
        true_values = ['true', 'True', 'TRUE', '1', 'yes', 'Yes', 'on', 'y']
        for value in true_values:
            assert parse_bool(value) is True, f"Failed for: {value}"

    def test_parse_false_values(self):
        """Parse various false values"""
        false_values = ['false', 'False', 'FALSE', '0', 'no', 'No', 'off', 'n', '']
        for value in false_values:
            assert parse_bool(value) is False, f"Failed for: {value}"

    def test_parse_bool_with_bool_input(self):
        """Parse when input is already boolean"""
        assert parse_bool(True) is True
        assert parse_bool(False) is False

    def test_parse_unexpected_value(self):
        """Unexpected value defaults to False"""
        assert parse_bool('invalid') is False


class TestParseInt:
    """Test integer parsing"""

    def test_parse_valid_int(self):
        """Parse valid integer strings"""
        assert parse_int('123') == 123
        assert parse_int('0') == 0
        assert parse_int('-456') == -456

    def test_parse_int_with_int_input(self):
        """Parse when input is already integer"""
        assert parse_int(123) == 123

    def test_parse_invalid_int(self):
        """Return None for invalid integer"""
        assert parse_int('invalid') is None
        assert parse_int('12.34') is None

    def test_parse_int_with_whitespace(self):
        """Parse integer with whitespace"""
        assert parse_int('  456  ') == 456


class TestParseList:
    """Test list parsing"""

    def test_parse_comma_separated(self):
        """Parse comma-separated values"""
        assert parse_list('a,b,c') == ['a', 'b', 'c']

    def test_parse_with_whitespace(self):
        """Parse and strip whitespace"""
        assert parse_list('a, b , c') == ['a', 'b', 'c']

    def test_parse_single_item(self):
        """Parse single item without comma"""
        assert parse_list('single') == ['single']

    def test_parse_empty_string(self):
        """Parse empty string to empty list"""
        assert parse_list('') == []

    def test_parse_list_with_list_input(self):
        """Return input if already a list"""
        assert parse_list(['a', 'b']) == ['a', 'b']


class TestMapEnvToConfig:
    """Test environment variable mapping"""

    def test_map_simple_var(self):
        """Map simple environment variable"""
        env_vars = {'TRACKER_TYPE': 'github'}
        config = map_env_to_config('TRACKER', env_vars)
        assert config == {'tracker': {'type': 'github'}}

    def test_map_nested_var(self):
        """Map nested environment variable"""
        env_vars = {
            'TRACKER_GITHUB_TOKEN': 'ghp_xxx',
            'TRACKER_GITHUB_ORGANIZATION': 'my-org'
        }
        config = map_env_to_config('TRACKER', env_vars)
        assert config == {
            'tracker': {
                'github': {
                    'token': 'ghp_xxx',
                    'organization': 'my-org'
                }
            }
        }

    def test_map_int_conversion(self):
        """Map and convert integer values"""
        env_vars = {'TRACKER_GITHUB_PROJECT_NUMBER': '5'}
        config = map_env_to_config('TRACKER', env_vars)
        assert config['tracker']['github']['project_number'] == 5
        assert isinstance(config['tracker']['github']['project_number'], int)

    def test_map_bool_conversion(self):
        """Map and convert boolean values"""
        env_vars = {'TRACKER_ENABLED': 'true'}
        config = map_env_to_config('TRACKER', env_vars)
        assert config['tracker']['enabled'] is True

    def test_map_list_conversion(self):
        """Map and convert list values"""
        env_vars = {'TRACKER_LABELS': 'bug,migration,automated'}
        config = map_env_to_config('TRACKER', env_vars)
        assert config['tracker']['labels'] == ['bug', 'migration', 'automated']

    def test_map_empty_env_vars(self):
        """Map with no matching environment variables"""
        config = map_env_to_config('TRACKER', {})
        assert config == {}

    def test_map_without_prefix(self):
        """Map without prefix filter"""
        env_vars = {'VAR1': 'value1', 'VAR2': 'value2'}
        config = map_env_to_config('', env_vars)
        assert config == {'var1': 'value1', 'var2': 'value2'}


class TestLoadConfigFromEnv:
    """Test load_config_from_env function"""

    def test_load_with_env_vars(self, monkeypatch):
        """Load configuration from environment"""
        monkeypatch.setenv('TRACKER_TYPE', 'github')
        monkeypatch.setenv('TRACKER_GITHUB_TOKEN', 'ghp_test')

        config = load_config_from_env('TRACKER')
        assert 'tracker' in config
        assert config['tracker']['type'] == 'github'

    def test_load_with_no_matching_vars(self, monkeypatch):
        """Load with no matching environment variables"""
        # Clear any TRACKER_ vars
        for key in list(os.environ.keys()):
            if key.startswith('TRACKER_'):
                monkeypatch.delenv(key, raising=False)

        config = load_config_from_env('TRACKER')
        assert config == {}


import os  # Add at top if missing

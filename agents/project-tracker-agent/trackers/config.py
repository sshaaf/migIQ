"""
Configuration validation and utilities for tracker integrations
"""

import logging
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from .env_mapper import load_config_from_env

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Exception raised for configuration validation errors"""
    pass


def resolve_env_var(value: str) -> str:
    """
    Resolve environment variable references in configuration values.

    Supports syntax:
    - $VAR_NAME: Resolved to environment variable value
    - $$LITERAL: Escaped dollar sign, becomes $LITERAL

    Args:
        value: Configuration value that may contain env var references

    Returns:
        Resolved value

    Raises:
        ConfigurationError: If referenced environment variable doesn't exist

    Examples:
        resolve_env_var("$GITHUB_TOKEN") -> value of GITHUB_TOKEN env var
        resolve_env_var("$$LITERAL") -> "$LITERAL"
        resolve_env_var("normal_value") -> "normal_value"
    """
    if not isinstance(value, str):
        return value

    # Handle escaped dollar sign
    if value.startswith('$$'):
        return value[1:]

    # Handle environment variable reference
    if value.startswith('$'):
        var_name = value[1:]
        env_value = os.environ.get(var_name)

        if env_value is None:
            raise ConfigurationError(
                f"Environment variable '{var_name}' is not set.\n"
                f"Please set it before running the tracker:\n"
                f"  export {var_name}=<value>"
            )

        return env_value

    # No substitution needed
    return value


def validate_tracker_config(config: Dict) -> bool:
    """
    Validate tracker configuration structure and required fields.

    Args:
        config: Full tracker configuration dictionary with structure:
            {
                "type": "local" | "github" | ...,
                "config": { ... }
            }

    Returns:
        True if valid

    Raises:
        ConfigurationError: If configuration is invalid
    """
    if not isinstance(config, dict):
        raise ConfigurationError("Tracker configuration must be a dictionary")

    tracker_type = config.get('type', 'local')

    # Validate based on tracker type
    if tracker_type == 'local':
        return _validate_local_config(config.get('config', {}))
    elif tracker_type == 'github':
        return _validate_github_config(config.get('config', {}))
    elif tracker_type in ('gitlab', 'jira'):
        logger.warning(f"Tracker type '{tracker_type}' is not yet implemented")
        return True
    else:
        logger.warning(f"Unknown tracker type '{tracker_type}', using local tracker")
        return True


def _validate_local_config(config: Dict) -> bool:
    """
    Validate local tracker configuration.

    Args:
        config: Local tracker config (all fields optional)

    Returns:
        True if valid
    """
    # Local tracker has no required fields
    # Validate optional fields if present
    if 'tasks_path' in config:
        if not isinstance(config['tasks_path'], str):
            raise ConfigurationError("tasks_path must be a string")

    return True


def _validate_github_config(config: Dict) -> bool:
    """
    Validate GitHub tracker configuration.

    Args:
        config: GitHub tracker config

    Returns:
        True if valid

    Raises:
        ConfigurationError: If required fields are missing or invalid
    """
    if not isinstance(config, dict):
        raise ConfigurationError(
            "GitHub tracker requires a 'config' dictionary.\n\n"
            "Example:\n"
            "{\n"
            '  "type": "github",\n'
            '  "config": {\n'
            '    "token": "$GITHUB_TOKEN",\n'
            '    "organization": "my-org"\n'
            "  }\n"
            "}\n\n"
            "Note: project_number is optional - will auto-create if not specified"
        )

    # Required fields (project_number is now optional)
    required_fields = ['token', 'organization']
    missing_fields = [field for field in required_fields if field not in config]

    if missing_fields:
        raise ConfigurationError(
            f"GitHub tracker configuration is missing required fields: {', '.join(missing_fields)}\n\n"
            "Required fields:\n"
            "  - token: GitHub personal access token (use $GITHUB_TOKEN for env var)\n"
            "  - organization: GitHub organization or username\n\n"
            "Optional fields:\n"
            "  - project_number: GitHub project number (will auto-create if not specified)\n"
            "  - project_name: Custom project name for auto-creation\n"
            "  - project_description: Project description\n\n"
            "Example:\n"
            "{\n"
            '  "type": "github",\n'
            '  "config": {\n'
            '    "token": "$GITHUB_TOKEN",\n'
            '    "organization": "my-org"\n'
            "  }\n"
            "}"
        )

    # Validate field types
    if not isinstance(config['token'], str):
        raise ConfigurationError("GitHub token must be a string")

    if not isinstance(config['organization'], str):
        raise ConfigurationError("GitHub organization must be a string")

    # Resolve token from environment variable if needed
    try:
        resolve_env_var(config['token'])
    except ConfigurationError as e:
        raise ConfigurationError(f"GitHub token error: {e}")

    # Warn if project_number not specified - auto-creation requires 'project' scope
    if 'project_number' not in config or config.get('project_number') is None:
        logger.warning(
            "No project_number specified - will auto-create GitHub project.\n"
            "Ensure your GitHub token has 'project' scope permission."
        )

    # Validate optional fields
    if 'project_number' in config and config['project_number'] is not None:
        if not isinstance(config['project_number'], int):
            raise ConfigurationError("GitHub project_number must be an integer")

    if 'project_name' in config:
        if not isinstance(config['project_name'], str):
            raise ConfigurationError("GitHub project_name must be a string")

    if 'project_description' in config:
        if not isinstance(config['project_description'], str):
            raise ConfigurationError("GitHub project_description must be a string")

    if 'labels' in config:
        if not isinstance(config['labels'], list):
            raise ConfigurationError("GitHub labels must be a list of strings")

    if 'default_assignee' in config:
        if not isinstance(config['default_assignee'], str):
            raise ConfigurationError("GitHub default_assignee must be a string")

    return True


def resolve_config_env_vars(config: Dict) -> Dict:
    """
    Recursively resolve environment variables in a configuration dictionary.

    Args:
        config: Configuration dictionary

    Returns:
        Configuration with resolved environment variables

    Raises:
        ConfigurationError: If any environment variable cannot be resolved
    """
    if not isinstance(config, dict):
        return config

    resolved = {}
    for key, value in config.items():
        if isinstance(value, str):
            resolved[key] = resolve_env_var(value)
        elif isinstance(value, dict):
            resolved[key] = resolve_config_env_vars(value)
        elif isinstance(value, list):
            resolved[key] = [
                resolve_env_var(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            resolved[key] = value

    return resolved


def load_tracker_config_from_env() -> Optional[Dict]:
    """
    Load tracker configuration from environment variables.

    Loads from .env file if present, then maps environment variables
    to tracker configuration structure.

    Returns:
        Tracker configuration dictionary or None if no env vars found

    Examples:
        With TRACKER_TYPE=github, TRACKER_GITHUB_TOKEN=xxx in environment:
        Returns: {
            'type': 'github',
            'config': {
                'token': 'xxx',
                ...
            }
        }
    """
    # Load .env file if present (doesn't override existing env vars)
    load_dotenv()

    # Load configuration from environment variables
    env_config = load_config_from_env('TRACKER')

    if not env_config or 'tracker' not in env_config:
        return None

    tracker_config = env_config['tracker']

    # Restructure to match expected format
    # From: {'type': 'github', 'github': {'token': 'xxx', ...}}
    # To: {'type': 'github', 'config': {'token': 'xxx', ...}}

    tracker_type = tracker_config.get('type', 'local')
    result = {'type': tracker_type}

    # Find the config section (matches tracker type)
    if tracker_type in tracker_config:
        result['config'] = tracker_config[tracker_type]
    elif 'local' in tracker_config:
        result['config'] = tracker_config['local']
    else:
        result['config'] = {}

    return result


def merge_configs(env_config: Optional[Dict], context_config: Optional[Dict]) -> Optional[Dict]:
    """
    Merge environment and context configurations with priority.

    Priority order (highest first):
    1. Explicit context configuration
    2. Environment variable configuration
    3. None (let factory use defaults)

    Args:
        env_config: Configuration from environment variables
        context_config: Configuration from JSON context

    Returns:
        Merged configuration dictionary or None

    Examples:
        merge_configs(None, {'type': 'github'}) -> {'type': 'github'}
        merge_configs({'type': 'local'}, {'type': 'github'}) -> {'type': 'github'}
        merge_configs({'type': 'local'}, None) -> {'type': 'local'}
    """
    # Context has highest priority - if explicitly provided, use it
    if context_config is not None:
        logger.info("Using tracker configuration from context (explicit priority)")
        return context_config

    # Fall back to environment configuration
    if env_config is not None:
        logger.info("Using tracker configuration from environment")
        return env_config

    # No configuration from either source
    logger.info("No tracker configuration found in environment or context, using defaults")
    return None

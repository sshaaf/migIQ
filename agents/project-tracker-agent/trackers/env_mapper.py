"""
Environment Variable Mapper

Maps flat environment variables to nested configuration dictionaries.
Supports type conversion (bool, int, list) and hierarchical key mapping.
"""

import logging
import os
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def parse_bool(value: str) -> bool:
    """
    Parse string value to boolean.

    Args:
        value: String value to parse

    Returns:
        Boolean value

    Examples:
        parse_bool("true") -> True
        parse_bool("1") -> True
        parse_bool("yes") -> True
        parse_bool("false") -> False
    """
    if isinstance(value, bool):
        return value

    value_lower = str(value).lower().strip()

    # True values
    if value_lower in ('true', '1', 'yes', 'on', 'y'):
        return True

    # False values
    if value_lower in ('false', '0', 'no', 'off', 'n', ''):
        return False

    # Default to False for unexpected values
    logger.warning(f"Unexpected boolean value '{value}', defaulting to False")
    return False


def parse_int(value: str) -> Optional[int]:
    """
    Parse string value to integer.

    Args:
        value: String value to parse

    Returns:
        Integer value or None if parsing fails

    Examples:
        parse_int("123") -> 123
        parse_int("invalid") -> None
    """
    if isinstance(value, int):
        return value

    try:
        return int(str(value).strip())
    except (ValueError, AttributeError):
        logger.warning(f"Failed to parse '{value}' as integer")
        return None


def parse_list(value: str) -> List[str]:
    """
    Parse comma-separated string to list.

    Args:
        value: Comma-separated string

    Returns:
        List of strings

    Examples:
        parse_list("a,b,c") -> ['a', 'b', 'c']
        parse_list("single") -> ['single']
        parse_list("") -> []
    """
    if isinstance(value, list):
        return value

    value_str = str(value).strip()

    if not value_str:
        return []

    # Split by comma and strip whitespace from each item
    return [item.strip() for item in value_str.split(',') if item.strip()]


def _detect_value_type(value: str) -> Any:
    """
    Detect and convert value to appropriate Python type.

    Args:
        value: String value from environment variable

    Returns:
        Converted value (int, bool, list, or str)
    """
    if not value:
        return value

    # Try integer
    int_value = parse_int(value)
    if int_value is not None:
        return int_value

    # Try boolean (check for common boolean strings)
    if value.lower() in ('true', 'false', '1', '0', 'yes', 'no', 'on', 'off'):
        return parse_bool(value)

    # Try list (contains comma)
    if ',' in value:
        return parse_list(value)

    # Default to string
    return value


def map_env_to_config(prefix: str = '', env_vars: Optional[Dict[str, str]] = None) -> Dict:
    """
    Map environment variables to nested configuration dictionary.

    Converts flat UPPER_CASE environment variables to nested lowercase dict:
    TRACKER_GITHUB_TOKEN -> {'tracker': {'github': {'token': 'value'}}}

    Args:
        prefix: Prefix to filter environment variables (e.g., 'TRACKER')
        env_vars: Optional dict of environment variables (defaults to os.environ)

    Returns:
        Nested configuration dictionary

    Examples:
        With TRACKER_TYPE=github in environment:
        map_env_to_config('TRACKER') -> {'tracker': {'type': 'github'}}

        With TRACKER_GITHUB_PROJECT_NUMBER=5:
        map_env_to_config('TRACKER') -> {
            'tracker': {
                'github': {
                    'project_number': 5
                }
            }
        }
    """
    if env_vars is None:
        env_vars = dict(os.environ)

    config: Dict = {}

    # Filter env vars by prefix if provided
    if prefix:
        prefix_upper = prefix.upper()
        if not prefix_upper.endswith('_'):
            prefix_upper += '_'

        filtered_vars = {
            k: v for k, v in env_vars.items()
            if k.startswith(prefix_upper)
        }
    else:
        filtered_vars = env_vars

    # Process each environment variable
    for key, value in filtered_vars.items():
        # Remove prefix if present
        if prefix:
            prefix_upper = prefix.upper() + '_'
            if key.startswith(prefix_upper):
                key = key[len(prefix_upper):]

        # Split key by underscore to create hierarchy
        parts = key.lower().split('_')

        # Navigate/create nested structure
        current = config
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set the value with type detection
        final_key = parts[-1]
        current[final_key] = _detect_value_type(value)

    return config


def load_config_from_env(prefix: str = 'TRACKER') -> Dict:
    """
    Load configuration from environment variables with specified prefix.

    This is the main entry point for loading config from environment.

    Args:
        prefix: Environment variable prefix (default: 'TRACKER')

    Returns:
        Configuration dictionary

    Examples:
        With environment:
          TRACKER_TYPE=github
          TRACKER_GITHUB_TOKEN=ghp_xxx
          TRACKER_GITHUB_ORGANIZATION=my-org
          TRACKER_GITHUB_PROJECT_NUMBER=5

        load_config_from_env('TRACKER') returns:
        {
            'tracker': {
                'type': 'github',
                'github': {
                    'token': 'ghp_xxx',
                    'organization': 'my-org',
                    'project_number': 5
                }
            }
        }
    """
    config = map_env_to_config(prefix)

    if config:
        logger.info(f"Loaded configuration from environment (prefix: {prefix})")
        logger.debug(f"Config keys: {list(config.keys())}")

    return config
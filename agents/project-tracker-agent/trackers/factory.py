"""
Tracker Factory - Creates tracker instances based on configuration
"""

import logging
from typing import Dict, Optional

from .interface import TrackerInterface

logger = logging.getLogger(__name__)


def create_tracker(config: Optional[Dict] = None) -> TrackerInterface:
    """
    Factory method to create appropriate tracker instance based on configuration.

    Args:
        config: Tracker configuration dictionary with structure:
            {
                "type": "local" | "github" | "gitlab" | "jira",
                "config": {
                    # Tracker-specific configuration
                }
            }

    Returns:
        TrackerInterface implementation

    Examples:
        Local tracker (default):
            create_tracker()
            create_tracker({"type": "local"})

        GitHub tracker:
            create_tracker({
                "type": "github",
                "config": {
                    "token": "$GITHUB_TOKEN",
                    "organization": "my-org",
                    "project_number": 5
                }
            })
    """
    # Default to local tracker if no config provided
    if config is None:
        logger.info("No tracker configuration provided, using LocalTracker")
        from .local_tracker import LocalTracker
        return LocalTracker()

    tracker_type = config.get('type', 'local').lower()
    tracker_config = config.get('config', {})

    if tracker_type == 'local':
        logger.info("Creating LocalTracker")
        from .local_tracker import LocalTracker
        return LocalTracker(tracker_config)

    elif tracker_type == 'github':
        logger.info("Creating GitHubProjectsTracker")
        from .github_tracker import GitHubProjectsTracker
        return GitHubProjectsTracker(tracker_config)

    elif tracker_type in ('gitlab', 'jira'):
        logger.warning(
            f"Tracker type '{tracker_type}' is not yet implemented. "
            f"Falling back to LocalTracker."
        )
        from .local_tracker import LocalTracker
        return LocalTracker()

    else:
        logger.error(
            f"Unknown tracker type: '{tracker_type}'. "
            f"Supported types: local, github, gitlab (planned), jira (planned). "
            f"Falling back to LocalTracker."
        )
        from .local_tracker import LocalTracker
        return LocalTracker()

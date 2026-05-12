"""
Tracker Integration Module

Provides abstraction for different project tracking backends:
- LocalTracker: tasks.md file-based tracking (default)
- GitHubProjectsTracker: GitHub Projects v2 integration
- Future: GitLab, Jira integrations
"""

from .interface import TrackerInterface
from .factory import create_tracker

__all__ = ['TrackerInterface', 'create_tracker']

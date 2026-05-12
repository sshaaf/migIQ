"""
TrackerInterface - Abstract base class for tracker implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class TrackerInterface(ABC):
    """
    Abstract interface for project tracker backends.

    All tracker implementations (LocalTracker, GitHubProjectsTracker, etc.)
    must implement these methods to provide consistent tracking capabilities.
    """

    @abstractmethod
    def create_issue(self, story_data: Dict) -> str:
        """
        Create a new issue/story in the tracker.

        Args:
            story_data: Dictionary containing story fields:
                - id: Story identifier (e.g., "US-001")
                - title: Story title
                - description: Story description
                - priority: Priority level (e.g., "P0", "P1")
                - story_points: Estimated story points
                - acceptance_criteria: List of acceptance criteria
                - affected_modules: List of affected modules
                - dependencies: List of dependency IDs
                - migration_type: Type of migration

        Returns:
            Issue ID or identifier from the tracker

        Raises:
            TrackerError: If issue creation fails
        """
        pass

    @abstractmethod
    def update_issue(self, issue_id: str, updates: Dict) -> bool:
        """
        Update an existing issue in the tracker.

        Args:
            issue_id: Tracker-specific issue identifier
            updates: Dictionary of fields to update:
                - status: New status value
                - story_points: Updated story points
                - assignee: Assigned user
                - Any other tracker-specific fields

        Returns:
            True if update succeeded, False otherwise

        Raises:
            TrackerError: If update fails
        """
        pass

    @abstractmethod
    def get_issue(self, issue_id: str) -> Dict:
        """
        Retrieve issue details from the tracker.

        Args:
            issue_id: Tracker-specific issue identifier

        Returns:
            Dictionary containing issue details

        Raises:
            TrackerError: If issue not found or retrieval fails
        """
        pass

    @abstractmethod
    def list_issues(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        List issues from the tracker with optional filtering.

        Args:
            filters: Optional dictionary of filter criteria:
                - status: Filter by status
                - priority: Filter by priority
                - assignee: Filter by assignee

        Returns:
            List of issue dictionaries

        Raises:
            TrackerError: If listing fails
        """
        pass

    @abstractmethod
    def sync_story(self, story: Dict) -> Dict:
        """
        Synchronize a complete user story to the tracker.

        This is a higher-level method that handles creating new issues
        or updating existing ones based on story state.

        Args:
            story: Complete story dictionary with all fields

        Returns:
            Dictionary containing sync results:
                - issue_id: Tracker issue ID
                - url: Link to tracker issue (if available)
                - status: Sync status
                - created: Boolean indicating if issue was created

        Raises:
            TrackerError: If sync fails
        """
        pass


class TrackerError(Exception):
    """Exception raised for tracker operation failures"""
    pass

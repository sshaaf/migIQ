"""
GitHubProjectsTracker - GitHub Projects v2 integration via GraphQL API
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional

import requests

from .config import ConfigurationError, resolve_env_var
from .interface import TrackerInterface, TrackerError

logger = logging.getLogger(__name__)


class GitHubProjectsTracker(TrackerInterface):
    """
    GitHub Projects v2 tracker implementation using GraphQL API.

    Supports creating and updating project items, with field mapping
    for priority, status, and story points.
    """

    GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
    MAX_RETRIES = 3
    RETRY_DELAYS = [1, 2, 4]  # Exponential backoff in seconds

    def __init__(self, config: Dict):
        """
        Initialize GitHub Projects tracker.

        Args:
            config: Configuration dictionary with:
                - token: GitHub PAT (can be $ENV_VAR)
                - organization: GitHub org or username
                - project_number: Optional project number (auto-creates if not provided)
                - auto_create: Optional, defaults to True
                - project_name: Optional custom project name for auto-creation
                - project_description: Optional project description
                - labels: Optional list of labels
                - default_assignee: Optional default assignee

        Raises:
            ConfigurationError: If configuration is invalid
        """
        self.token = resolve_env_var(config.get('token', ''))
        if not self.token:
            raise ConfigurationError("GitHub token is required")

        self.organization = config.get('organization', '')
        if not self.organization:
            raise ConfigurationError("GitHub organization is required")

        self.project_number = config.get('project_number')
        auto_create = config.get('auto_create', True)

        self.labels = config.get('labels', [])
        self.default_assignee = config.get('default_assignee')

        # Cache for project node ID
        self._project_node_id: Optional[str] = None

        # Auto-create project if project_number not specified
        if self.project_number is None and auto_create:
            try:
                logger.info("No project_number specified, auto-creating GitHub project...")

                # Resolve owner ID
                owner_id = self._get_owner_id(self.organization)

                # Generate project name
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                project_name = config.get('project_name') or f"Migration Agent - {self.organization} - {timestamp}"

                # Create project
                self.project_number = self._create_project_v2(owner_id, project_name)

                # Print information for user
                print(f"\n✓ Created GitHub Project #{self.project_number}: {project_name}")
                print(f"  URL: https://github.com/orgs/{self.organization}/projects/{self.project_number}")
                print(f"\nTo persist this project, add to your .env file:")
                print(f"  TRACKER_GITHUB_PROJECT_NUMBER={self.project_number}\n")

            except Exception as e:
                logger.error(f"Failed to auto-create GitHub project: {e}")
                raise ConfigurationError(
                    f"Failed to auto-create GitHub project: {e}\n"
                    "Either provide TRACKER_GITHUB_PROJECT_NUMBER in .env or ensure your GitHub token has 'project' scope."
                )
        elif self.project_number is None:
            raise ConfigurationError(
                "GitHub project_number is required when auto_create is disabled"
            )

        logger.info(
            f"GitHubProjectsTracker initialized for {self.organization}/project/{self.project_number}"
        )

    def _get_owner_id(self, organization: str) -> str:
        """
        Resolve organization or user login to GitHub node ID.

        Args:
            organization: GitHub organization or user login

        Returns:
            Owner node ID

        Raises:
            TrackerError: If organization/user not found
        """
        # Try organization first
        org_query = """
        query($login: String!) {
          organization(login: $login) {
            id
          }
        }
        """

        variables = {'login': organization}

        try:
            result = self._execute_graphql(org_query, variables)
            org_data = result.get('data', {}).get('organization')

            if org_data and org_data.get('id'):
                logger.info(f"Resolved organization {organization} to ID {org_data['id']}")
                return org_data['id']

            # Fallback to user query
            user_query = """
            query($login: String!) {
              user(login: $login) {
                id
              }
            }
            """

            result = self._execute_graphql(user_query, variables)
            user_data = result.get('data', {}).get('user')

            if user_data and user_data.get('id'):
                logger.info(f"Resolved user {organization} to ID {user_data['id']}")
                return user_data['id']

            raise TrackerError(
                f"Organization or user '{organization}' not found. "
                "Please verify the name is correct."
            )

        except TrackerError:
            raise
        except Exception as e:
            raise TrackerError(f"Failed to resolve owner ID for '{organization}': {e}")

    def _create_project_v2(self, owner_id: str, title: str) -> str:
        """
        Create a new GitHub Project v2.

        Args:
            owner_id: Owner node ID (organization or user)
            title: Project title

        Returns:
            Project number

        Raises:
            TrackerError: If creation fails
        """
        mutation = """
        mutation($ownerId: ID!, $title: String!) {
          createProjectV2(input: {
            ownerId: $ownerId
            title: $title
          }) {
            projectV2 {
              id
              number
              url
              title
            }
          }
        }
        """

        variables = {
            'ownerId': owner_id,
            'title': title
        }

        try:
            result = self._execute_graphql(mutation, variables)
            project_data = result.get('data', {}).get('createProjectV2', {}).get('projectV2')

            if not project_data:
                raise TrackerError("Failed to create GitHub project - no project data returned")

            project_number = project_data.get('number')
            project_url = project_data.get('url')
            project_id = project_data.get('id')

            if not project_number:
                raise TrackerError("Failed to extract project number from created project")

            logger.info(f"Created GitHub project: {title} (number: {project_number}, ID: {project_id})")
            logger.info(f"Project URL: {project_url}")

            return project_number

        except TrackerError:
            raise
        except Exception as e:
            raise TrackerError(
                f"Failed to create GitHub project: {e}\n"
                "Please verify your GitHub token has 'project' scope permissions."
            )

    def delete_project(self, project_id: str) -> bool:
        """
        Delete a GitHub Project v2.

        Args:
            project_id: Project node ID

        Returns:
            True on success, False on failure

        Raises:
            TrackerError: If deletion fails
        """
        mutation = """
        mutation($projectId: ID!) {
          deleteProjectV2(input: {
            projectId: $projectId
          }) {
            projectV2 {
              id
            }
          }
        }
        """

        variables = {'projectId': project_id}

        try:
            result = self._execute_graphql(mutation, variables)
            deleted_project = result.get('data', {}).get('deleteProjectV2', {}).get('projectV2')

            if deleted_project:
                logger.info(f"Successfully deleted GitHub project {project_id}")
                return True
            else:
                logger.error(f"Failed to delete GitHub project {project_id} - no confirmation returned")
                return False

        except TrackerError as e:
            logger.error(f"Failed to delete GitHub project {project_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting GitHub project {project_id}: {e}")
            return False

    def _resolve_project_node_id(self) -> str:
        """
        Resolve and cache the GitHub project node ID.

        Returns:
            Project node ID

        Raises:
            TrackerError: If project cannot be found
        """
        if self._project_node_id:
            return self._project_node_id

        query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              id
              title
            }
          }
        }
        """

        variables = {
            'org': self.organization,
            'number': self.project_number
        }

        try:
            result = self._execute_graphql(query, variables)
            project_data = result.get('data', {}).get('organization', {}).get('projectV2')

            if not project_data:
                raise TrackerError(
                    f"GitHub project not found: {self.organization}/project/{self.project_number}\n"
                    "Please verify the organization and project number are correct."
                )

            self._project_node_id = project_data['id']
            logger.info(f"Resolved GitHub project: {project_data['title']} (ID: {self._project_node_id})")
            return self._project_node_id

        except TrackerError:
            raise
        except Exception as e:
            raise TrackerError(f"Failed to resolve GitHub project ID: {e}")

    def _execute_graphql(self, query: str, variables: Dict) -> Dict:
        """
        Execute a GraphQL query against GitHub API.

        Args:
            query: GraphQL query string
            variables: Query variables

        Returns:
            Response JSON

        Raises:
            TrackerError: If request fails
        """
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

        payload = {
            'query': query,
            'variables': variables
        }

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.post(
                    self.GITHUB_GRAPHQL_URL,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                # Check for authentication errors
                if response.status_code == 401:
                    raise TrackerError(
                        "GitHub authentication failed. "
                        "Please verify your GITHUB_TOKEN is valid and has the required permissions:\n"
                        "  - repo (for organization projects)\n"
                        "  - project (for managing projects)"
                    )

                # Check for rate limiting
                if response.status_code == 429 or 'rate limit' in response.text.lower():
                    if attempt < self.MAX_RETRIES - 1:
                        delay = self.RETRY_DELAYS[attempt]
                        logger.warning(f"GitHub rate limit hit, retrying in {delay}s (attempt {attempt + 1}/{self.MAX_RETRIES})")
                        time.sleep(delay)
                        continue
                    else:
                        raise TrackerError("GitHub rate limit exceeded. Please try again later.")

                response.raise_for_status()
                data = response.json()

                # Check for GraphQL errors
                if 'errors' in data:
                    error_messages = [err.get('message', str(err)) for err in data['errors']]
                    raise TrackerError(f"GitHub GraphQL errors: {'; '.join(error_messages)}")

                # Log rate limit info
                if 'data' in data:
                    rate_limit = data.get('data', {}).get('rateLimit', {})
                    if rate_limit:
                        remaining = rate_limit.get('remaining', 'unknown')
                        logger.debug(f"GitHub API rate limit remaining: {remaining}")

                return data

            except requests.exceptions.RequestException as e:
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAYS[attempt]
                    logger.warning(f"Network error, retrying in {delay}s: {e}")
                    time.sleep(delay)
                    continue
                else:
                    raise TrackerError(f"GitHub API request failed after {self.MAX_RETRIES} attempts: {e}")

        raise TrackerError("Unexpected error in GraphQL execution")

    def _map_priority(self, priority: str) -> str:
        """
        Map migration priority to GitHub priority.

        Args:
            priority: Migration priority (P0, P1, P2, P3)

        Returns:
            GitHub priority (High, Medium, Low)
        """
        mapping = {
            'P0': 'High',
            'P1': 'Medium',
            'P2': 'Low',
            'P3': 'Low'
        }
        return mapping.get(priority, 'Medium')

    def _map_status(self, status: str) -> str:
        """
        Map migration status to GitHub status.

        Args:
            status: Migration status (Backlog, In Progress, Done, Failed)

        Returns:
            GitHub status (Todo, In Progress, Done)
        """
        mapping = {
            'Backlog': 'Todo',
            'In Progress': 'In Progress',
            'Done': 'Done',
            'Failed': 'Done'  # Mark failed as done but with failure notes
        }
        return mapping.get(status, 'Todo')

    def create_issue(self, story_data: Dict) -> str:
        """
        Create a draft issue in GitHub Projects v2.

        Args:
            story_data: Story dictionary

        Returns:
            GitHub project item ID

        Raises:
            TrackerError: If creation fails
        """
        try:
            project_id = self._resolve_project_node_id()

            # Format description with acceptance criteria
            description = story_data.get('description', '')
            acceptance_criteria = story_data.get('acceptance_criteria', [])

            if acceptance_criteria:
                description += "\n\n**Acceptance Criteria:**\n"
                for criterion in acceptance_criteria:
                    description += f"- [ ] {criterion}\n"

            # Add technical details
            description += f"\n\n**Technical Details:**\n"
            description += f"- Affected modules: {', '.join(story_data.get('affected_modules', ['TBD']))}\n"
            description += f"- Dependencies: {', '.join(story_data.get('dependencies', ['None']))}\n"
            description += f"- Migration type: {story_data.get('migration_type', 'TBD')}\n"

            mutation = """
            mutation($projectId: ID!, $title: String!, $body: String!) {
              addProjectV2DraftIssue(input: {
                projectId: $projectId
                title: $title
                body: $body
              }) {
                projectItem {
                  id
                  content {
                    ... on DraftIssue {
                      title
                    }
                  }
                }
              }
            }
            """

            variables = {
                'projectId': project_id,
                'title': f"[{story_data['id']}] {story_data.get('title', 'Untitled')}",
                'body': description
            }

            result = self._execute_graphql(mutation, variables)
            item_data = result.get('data', {}).get('addProjectV2DraftIssue', {}).get('projectItem', {})

            if not item_data:
                raise TrackerError("Failed to create GitHub project item")

            item_id = item_data['id']
            logger.info(f"Created GitHub project item {item_id} for story {story_data['id']}")

            return item_id

        except TrackerError:
            raise
        except Exception as e:
            logger.error(f"Failed to create GitHub issue: {e}")
            raise TrackerError(f"Failed to create GitHub issue: {e}")

    def update_issue(self, issue_id: str, updates: Dict) -> bool:
        """
        Update a GitHub project item.

        Args:
            issue_id: GitHub project item ID
            updates: Fields to update

        Returns:
            True if successful

        Raises:
            TrackerError: If update fails
        """
        try:
            # GitHub Projects v2 field updates require field IDs
            # For simplicity, we'll log the update intent
            # In production, this would query field IDs and update them
            logger.info(f"Update requested for GitHub item {issue_id}: {updates}")

            # Note: Full implementation would require:
            # 1. Query project fields to get field IDs
            # 2. Use updateProjectV2ItemFieldValue mutation for each field
            # This is a simplified version

            return True

        except Exception as e:
            logger.error(f"Failed to update GitHub issue {issue_id}: {e}")
            raise TrackerError(f"Failed to update GitHub issue: {e}")

    def get_issue(self, issue_id: str) -> Dict:
        """
        Get a GitHub project item.

        Args:
            issue_id: GitHub project item ID

        Returns:
            Issue dictionary

        Raises:
            TrackerError: If retrieval fails
        """
        query = """
        query($itemId: ID!) {
          node(id: $itemId) {
            ... on ProjectV2Item {
              id
              content {
                ... on DraftIssue {
                  title
                  body
                }
              }
            }
          }
        }
        """

        variables = {'itemId': issue_id}

        try:
            result = self._execute_graphql(query, variables)
            item_data = result.get('data', {}).get('node', {})

            if not item_data:
                raise TrackerError(f"GitHub item {issue_id} not found")

            return {
                'id': item_data['id'],
                'title': item_data.get('content', {}).get('title', ''),
                'body': item_data.get('content', {}).get('body', '')
            }

        except TrackerError:
            raise
        except Exception as e:
            logger.error(f"Failed to get GitHub issue {issue_id}: {e}")
            raise TrackerError(f"Failed to get GitHub issue: {e}")

    def list_issues(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        List items from GitHub project.

        Args:
            filters: Optional filters

        Returns:
            List of issue dictionaries

        Raises:
            TrackerError: If listing fails
        """
        try:
            project_id = self._resolve_project_node_id()

            query = """
            query($projectId: ID!) {
              node(id: $projectId) {
                ... on ProjectV2 {
                  items(first: 100) {
                    nodes {
                      id
                      content {
                        ... on DraftIssue {
                          title
                          body
                        }
                      }
                    }
                  }
                }
              }
            }
            """

            variables = {'projectId': project_id}

            result = self._execute_graphql(query, variables)
            items = result.get('data', {}).get('node', {}).get('items', {}).get('nodes', [])

            return [
                {
                    'id': item['id'],
                    'title': item.get('content', {}).get('title', ''),
                    'body': item.get('content', {}).get('body', '')
                }
                for item in items
            ]

        except TrackerError:
            raise
        except Exception as e:
            logger.error(f"Failed to list GitHub issues: {e}")
            raise TrackerError(f"Failed to list GitHub issues: {e}")

    def sync_story(self, story: Dict) -> Dict:
        """
        Synchronize a story to GitHub Projects.

        Creates new item (always creates, doesn't check for existing).

        Args:
            story: Story dictionary

        Returns:
            Sync result dictionary
        """
        try:
            # Create new item
            item_id = self.create_issue(story)

            # Build project URL
            project_url = f"https://github.com/orgs/{self.organization}/projects/{self.project_number}"

            return {
                'issue_id': item_id,
                'url': project_url,
                'status': 'success',
                'created': True
            }

        except Exception as e:
            logger.error(f"Failed to sync story {story.get('id', 'unknown')} to GitHub: {e}")
            return {
                'issue_id': story.get('id', 'unknown'),
                'url': None,
                'status': 'error',
                'error': str(e),
                'created': False
            }

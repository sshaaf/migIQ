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
                - repository: Optional repository (owner/repo) for creating real issues
                              If not provided, attempts to auto-detect from git remote
                - project_path: Optional project path for auto-detecting repository
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

        # Repository for creating real issues
        # Try to auto-detect from git remote if not explicitly provided
        self.repository = config.get('repository')
        project_path = config.get('project_path')

        if not self.repository and project_path:
            try:
                detected_repo = self._detect_repository_from_git(project_path)
                if detected_repo:
                    self.repository = detected_repo
                    logger.info(f"Auto-detected repository from git remote: {self.repository}")
                    print(f"✓ Auto-detected GitHub repository: {self.repository}")
            except Exception as e:
                logger.debug(f"Could not auto-detect repository: {e}")
                # Not an error - just means we'll use draft issues

        self._repository_id: Optional[str] = None  # Cache for repository node ID

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

                # Show appropriate URL based on repository config
                if self.repository:
                    print(f"  URL: https://github.com/{self.repository}/projects/{self.project_number}")
                    print(f"  Mode: Repository issues (issues created in {self.repository})")
                else:
                    print(f"  URL: https://github.com/orgs/{self.organization}/projects/{self.project_number}")
                    print(f"  Mode: Draft issues (project-only items)")

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

    def _detect_repository_from_git(self, project_path: str) -> Optional[str]:
        """
        Auto-detect GitHub repository from git remote URL.

        Args:
            project_path: Path to project directory

        Returns:
            Repository in "owner/repo" format, or None if not detected

        Examples:
            git@github.com:my-org/my-repo.git -> "my-org/my-repo"
            https://github.com/my-org/my-repo.git -> "my-org/my-repo"
        """
        import subprocess
        import re

        try:
            # Get git remote origin URL
            result = subprocess.run(
                ['git', '-C', project_path, 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return None

            remote_url = result.stdout.strip()

            # Parse GitHub repository from URL
            # Supports both SSH and HTTPS formats:
            # - git@github.com:owner/repo.git
            # - https://github.com/owner/repo.git
            # - https://github.com/owner/repo

            # SSH format: git@github.com:owner/repo.git
            ssh_match = re.match(r'git@github\.com:([^/]+)/(.+?)(?:\.git)?$', remote_url)
            if ssh_match:
                owner, repo = ssh_match.groups()
                return f"{owner}/{repo}"

            # HTTPS format: https://github.com/owner/repo.git
            https_match = re.match(r'https://github\.com/([^/]+)/(.+?)(?:\.git)?$', remote_url)
            if https_match:
                owner, repo = https_match.groups()
                return f"{owner}/{repo}"

            logger.debug(f"Could not parse GitHub repo from remote URL: {remote_url}")
            return None

        except subprocess.TimeoutExpired:
            logger.debug("git command timed out")
            return None
        except FileNotFoundError:
            logger.debug("git command not found")
            return None
        except Exception as e:
            logger.debug(f"Failed to detect repository: {e}")
            return None

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

    def _get_repository_id(self, repository: str) -> str:
        """
        Resolve repository (owner/repo) to GitHub node ID.

        Args:
            repository: Repository in format "owner/repo"

        Returns:
            Repository node ID

        Raises:
            TrackerError: If repository not found
        """
        if self._repository_id:
            return self._repository_id

        # Parse owner/repo
        parts = repository.split('/')
        if len(parts) != 2:
            raise ConfigurationError(
                f"Invalid repository format '{repository}'. Expected 'owner/repo'"
            )

        owner, name = parts

        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
          }
        }
        """

        variables = {'owner': owner, 'name': name}

        try:
            result = self._execute_graphql(query, variables)
            repo_data = result.get('data', {}).get('repository')

            if not repo_data or not repo_data.get('id'):
                raise TrackerError(
                    f"Repository '{repository}' not found. "
                    "Please verify the owner and repository name are correct."
                )

            self._repository_id = repo_data['id']
            logger.info(f"Resolved repository {repository} to ID {self._repository_id}")
            return self._repository_id

        except TrackerError:
            raise
        except Exception as e:
            raise TrackerError(f"Failed to resolve repository ID for '{repository}': {e}")

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
        Create an issue - either as a repository issue or draft issue.

        If repository is configured, creates a real GitHub issue in that repository
        and links it to the project. Otherwise, creates a draft issue in the project.

        Args:
            story_data: Story dictionary

        Returns:
            GitHub project item ID

        Raises:
            TrackerError: If creation fails
        """
        try:
            if self.repository:
                # Create real repository issue + link to project
                return self._create_repository_issue(story_data)
            else:
                # Create draft issue in project only
                return self._create_draft_issue(story_data)

        except TrackerError:
            raise
        except Exception as e:
            logger.error(f"Failed to create GitHub issue: {e}")
            raise TrackerError(f"Failed to create GitHub issue: {e}")

    def _create_draft_issue(self, story_data: Dict) -> str:
        """Create a draft issue in GitHub Projects v2 (project-only)."""
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
            raise TrackerError("Failed to create GitHub project draft issue")

        item_id = item_data['id']
        logger.info(f"Created GitHub draft issue {item_id} for story {story_data['id']}")

        return item_id

    def _create_repository_issue(self, story_data: Dict) -> str:
        """Create a real GitHub repository issue and link it to the project."""
        repo_id = self._get_repository_id(self.repository)
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

        # Step 1: Create repository issue
        create_issue_mutation = """
        mutation($repositoryId: ID!, $title: String!, $body: String!) {
          createIssue(input: {
            repositoryId: $repositoryId
            title: $title
            body: $body
          }) {
            issue {
              id
              number
              url
            }
          }
        }
        """

        issue_variables = {
            'repositoryId': repo_id,
            'title': f"[{story_data['id']}] {story_data.get('title', 'Untitled')}",
            'body': description
        }

        result = self._execute_graphql(create_issue_mutation, issue_variables)
        issue_data = result.get('data', {}).get('createIssue', {}).get('issue', {})

        if not issue_data:
            raise TrackerError("Failed to create GitHub repository issue")

        issue_id = issue_data['id']
        issue_number = issue_data['number']
        issue_url = issue_data['url']

        logger.info(f"Created GitHub issue #{issue_number} for story {story_data['id']}: {issue_url}")

        # Step 2: Link issue to project
        link_mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {
            projectId: $projectId
            contentId: $contentId
          }) {
            item {
              id
            }
          }
        }
        """

        link_variables = {
            'projectId': project_id,
            'contentId': issue_id
        }

        result = self._execute_graphql(link_mutation, link_variables)
        item_data = result.get('data', {}).get('addProjectV2ItemById', {}).get('item', {})

        if not item_data:
            logger.warning(f"Created issue {issue_url} but failed to link to project")
            # Return issue ID anyway - issue was created successfully
            return issue_id

        item_id = item_data['id']
        logger.info(f"Linked issue #{issue_number} to project (item ID: {item_id})")

        return item_id

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

    def add_comment(self, issue_id: str, comment: str) -> bool:
        """
        Add a comment to a GitHub issue.

        Note: Only works for repository issues (created with TRACKER_GITHUB_REPOSITORY).
        Draft issues (project-only) do not support comments via API.

        Args:
            issue_id: GitHub issue node ID (starts with 'I_' for issues, 'DI_' for draft issues)
            comment: Comment text (markdown supported)

        Returns:
            True if comment added successfully, False otherwise

        Raises:
            TrackerError: If adding comment fails
        """
        # Check if this is a draft issue (they don't support comments)
        if issue_id.startswith('DI_') or issue_id.startswith('PVTI_'):
            logger.warning(
                f"Cannot add comments to draft issues (ID: {issue_id}). "
                "Configure TRACKER_GITHUB_REPOSITORY to create real issues with comment support."
            )
            return False

        try:
            mutation = """
            mutation($subjectId: ID!, $body: String!) {
              addComment(input: {
                subjectId: $subjectId
                body: $body
              }) {
                commentEdge {
                  node {
                    id
                    createdAt
                  }
                }
              }
            }
            """

            variables = {
                'subjectId': issue_id,
                'body': comment
            }

            result = self._execute_graphql(mutation, variables)
            comment_data = result.get('data', {}).get('addComment', {}).get('commentEdge', {}).get('node', {})

            if not comment_data:
                raise TrackerError("Failed to add comment - no response data")

            logger.info(f"Added comment to issue {issue_id}")
            return True

        except TrackerError:
            raise
        except Exception as e:
            logger.error(f"Failed to add comment to issue {issue_id}: {e}")
            raise TrackerError(f"Failed to add comment: {e}")

    def attach_output(self, issue_id: str, output_path: str, description: str = None) -> bool:
        """
        Attach output file content to GitHub issue as a formatted comment.

        Args:
            issue_id: GitHub issue node ID
            output_path: Path to output file
            description: Optional description

        Returns:
            True if attachment succeeded
        """
        try:
            import os
            import json

            if not os.path.exists(output_path):
                logger.warning(f"Output file not found: {output_path}")
                return False

            # Read file content
            with open(output_path, 'r') as f:
                content = f.read()

            # Determine file type for syntax highlighting
            file_ext = os.path.splitext(output_path)[1].lower()
            if file_ext == '.json':
                syntax = 'json'
                # Pretty print JSON
                try:
                    parsed = json.loads(content)
                    content = json.dumps(parsed, indent=2)
                except:
                    pass
            elif file_ext == '.md':
                syntax = 'markdown'
            else:
                syntax = ''

            # Format comment with file content
            comment = f"""## 📎 Output Attached

**File:** `{os.path.basename(output_path)}`
"""

            if description:
                comment += f"**Description:** {description}\n\n"

            # Truncate very large files
            max_size = 50000  # ~50KB
            if len(content) > max_size:
                comment += f"""
<details>
<summary>View Output (truncated - showing first {max_size} characters)</summary>

```{syntax}
{content[:max_size]}
...
(truncated)
```
</details>
"""
            else:
                comment += f"""
<details>
<summary>View Output</summary>

```{syntax}
{content}
```
</details>
"""

            comment += f"\n---\n*Attached automatically by migration agent*"

            # Add as comment
            return self.add_comment(issue_id, comment)

        except Exception as e:
            logger.error(f"Failed to attach output {output_path} to issue {issue_id}: {e}")
            return False
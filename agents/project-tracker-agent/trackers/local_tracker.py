"""
LocalTracker - tasks.md file-based tracker implementation
"""

import fcntl
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .interface import TrackerInterface, TrackerError

logger = logging.getLogger(__name__)


class LocalTracker(TrackerInterface):
    """
    Local file-based tracker using tasks.md for storage.

    This is the default tracker that maintains backward compatibility
    with the existing tasks.md format.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize LocalTracker.

        Args:
            config: Optional configuration dictionary:
                - tasks_path: Path to tasks.md file (default: ./tasks.md)
        """
        config = config or {}
        self.tasks_path = config.get('tasks_path', './tasks.md')
        logger.info(f"LocalTracker initialized with tasks_path: {self.tasks_path}")

    def read_tasks(self) -> str:
        """Read entire tasks.md file"""
        if not os.path.exists(self.tasks_path):
            raise FileNotFoundError(f"Tasks file not found: {self.tasks_path}")

        with open(self.tasks_path, 'r') as f:
            return f.read()

    def write_tasks(self, content: str):
        """Write tasks.md file with file locking"""
        # Ensure parent directory exists
        Path(self.tasks_path).parent.mkdir(parents=True, exist_ok=True)

        # Write with file locking to prevent concurrent write corruption
        with open(self.tasks_path, 'w') as f:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                f.write(content)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def parse_user_stories(self, content: str) -> List[Dict]:
        """Parse user stories from tasks.md content"""
        stories = []

        # Find all user story sections
        story_pattern = r'### \[(US-\d+)\] ([^\n]+)\n\n\*\*Priority\*\*: (P\d)\n\*\*Status\*\*: ([^\n]+)\n\*\*Story Points\*\*: (\d+)'

        matches = re.finditer(story_pattern, content)

        for match in matches:
            story_id = match.group(1)
            title = match.group(2)
            priority = match.group(3)
            status = match.group(4)
            story_points = int(match.group(5))

            stories.append({
                'id': story_id,
                'title': title,
                'priority': priority,
                'status': status,
                'story_points': story_points
            })

        return stories

    def create_issue(self, story_data: Dict) -> str:
        """
        Create a new user story in tasks.md.

        Args:
            story_data: Story dictionary with fields

        Returns:
            Story ID
        """
        try:
            content = self.read_tasks()

            # Find the "User Stories" section
            if "## User Stories" not in content:
                content += "\n\n## User Stories\n\n"

            stories_section_start = content.find("## User Stories")
            before_stories = content[:stories_section_start + len("## User Stories")]
            after_stories_marker = content.find("\n## ", stories_section_start + len("## User Stories"))

            if after_stories_marker == -1:
                after_stories = ""
            else:
                after_stories = content[after_stories_marker:]

            # Generate new story section
            story_id = story_data['id']
            new_story = f"""

### [{story_id}] {story_data.get('title', 'Untitled')}

**Priority**: {story_data.get('priority', 'P2')}
**Status**: {story_data.get('status', 'Backlog')}
**Story Points**: {story_data.get('story_points', 5)}
**Assigned To**: {story_data.get('assignee', 'Unassigned')}

**Description**:
{story_data.get('description', 'TBD')}

**Acceptance Criteria**:
"""
            for criterion in story_data.get('acceptance_criteria', []):
                new_story += f"- [ ] {criterion}\n"

            new_story += f"""
**Technical Details**:
- Affected modules: {', '.join(story_data.get('affected_modules', ['TBD']))}
- Dependencies: {', '.join(story_data.get('dependencies', ['None']))}
- Migration type: {story_data.get('migration_type', 'TBD')}

**Tasks**:
1. [ ] Analyze code
2. [ ] Generate characterization tests
3. [ ] Generate functional tests
4. [ ] Apply refactoring rules
5. [ ] Run benchmarks
6. [ ] Validate quality
7. [ ] Create merge request

**Notes**:
- Created by tracker
- Session: {story_data.get('session_id', 'N/A')}

**Links**:
- Kanban: (pending)
- MR: (pending)
- CI Pipeline: (pending)

---

"""

            # Combine sections
            updated_content = before_stories + new_story + after_stories
            self.write_tasks(updated_content)

            logger.info(f"Created issue {story_id} in tasks.md")
            return story_id

        except Exception as e:
            logger.error(f"Failed to create issue: {e}")
            raise TrackerError(f"Failed to create issue in tasks.md: {e}")

    def update_issue(self, issue_id: str, updates: Dict) -> bool:
        """
        Update an existing story in tasks.md.

        Args:
            issue_id: Story ID (e.g., "US-001")
            updates: Dictionary of fields to update

        Returns:
            True if successful
        """
        try:
            content = self.read_tasks()
            updated = False

            # Handle status updates
            if 'status' in updates:
                status = updates['status']
                content = self._update_story_status(content, issue_id, status)
                updated = True

            # Handle story points updates
            if 'story_points' in updates:
                pattern = rf'(### \[{issue_id}\][^\n]+\n\n(?:.*?\n)*?\*\*Story Points\*\*: )\d+'
                replacement = rf'\g<1>{updates["story_points"]}'
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                if new_content != content:
                    content = new_content
                    updated = True

            if updated:
                self.write_tasks(content)
                logger.info(f"Updated issue {issue_id} in tasks.md")

            return updated

        except Exception as e:
            logger.error(f"Failed to update issue {issue_id}: {e}")
            raise TrackerError(f"Failed to update issue {issue_id}: {e}")

    def _update_story_status(self, content: str, story_id: str, status: str) -> str:
        """Update story status in content"""
        # Find story section
        story_pattern = rf'(### \[{story_id}\][^\n]+\n\n)((?:.*?\n)*?)(\*\*Tasks\*\*:)'

        def replace_story(match):
            header = match.group(1)
            details = match.group(2)
            tasks_header = match.group(3)

            # Update status in details
            details = re.sub(
                r'\*\*Status\*\*: [^\n]+',
                f'**Status**: {status}',
                details
            )

            return f'{header}{details}{tasks_header}'

        return re.sub(story_pattern, replace_story, content, flags=re.DOTALL)

    def get_issue(self, issue_id: str) -> Dict:
        """
        Get a single story from tasks.md.

        Args:
            issue_id: Story ID

        Returns:
            Story dictionary
        """
        try:
            content = self.read_tasks()
            stories = self.parse_user_stories(content)

            for story in stories:
                if story['id'] == issue_id:
                    return story

            raise TrackerError(f"Issue {issue_id} not found in tasks.md")

        except FileNotFoundError as e:
            raise TrackerError(f"Tasks file not found: {e}")
        except Exception as e:
            logger.error(f"Failed to get issue {issue_id}: {e}")
            raise TrackerError(f"Failed to get issue {issue_id}: {e}")

    def list_issues(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        List all stories from tasks.md.

        Args:
            filters: Optional filters (status, priority, etc.)

        Returns:
            List of story dictionaries
        """
        try:
            content = self.read_tasks()
            stories = self.parse_user_stories(content)

            # Apply filters if provided
            if filters:
                if 'status' in filters:
                    stories = [s for s in stories if s['status'] == filters['status']]
                if 'priority' in filters:
                    stories = [s for s in stories if s['priority'] == filters['priority']]

            return stories

        except FileNotFoundError:
            logger.warning(f"Tasks file not found: {self.tasks_path}, returning empty list")
            return []
        except Exception as e:
            logger.error(f"Failed to list issues: {e}")
            raise TrackerError(f"Failed to list issues: {e}")

    def sync_story(self, story: Dict) -> Dict:
        """
        Synchronize a story to tasks.md.

        Creates new story if it doesn't exist, updates if it does.

        Args:
            story: Story dictionary

        Returns:
            Sync result dictionary
        """
        try:
            story_id = story['id']

            # Check if story exists
            try:
                existing = self.get_issue(story_id)
                # Update existing story
                self.update_issue(story_id, {
                    'status': story.get('status', existing['status']),
                    'story_points': story.get('story_points', existing['story_points'])
                })
                created = False
            except TrackerError:
                # Create new story
                self.create_issue(story)
                created = True

            return {
                'issue_id': story_id,
                'url': None,  # Local tracker doesn't have URLs
                'status': 'success',
                'created': created
            }

        except Exception as e:
            logger.error(f"Failed to sync story {story.get('id', 'unknown')}: {e}")
            return {
                'issue_id': story.get('id', 'unknown'),
                'url': None,
                'status': 'error',
                'error': str(e),
                'created': False
            }
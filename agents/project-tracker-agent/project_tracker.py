#!/usr/bin/env python3
"""
Project Tracker Agent Implementation

Main coordinator for migration workflow. Receives context from /migration skill,
executes initial tasks, and orchestrates user stories through the mesh.
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv

from trackers import create_tracker
from trackers.interface import TrackerError
from trackers.config import load_tracker_config_from_env, merge_configs

# Load .env file if present (also loads .env.local for overrides)
load_dotenv()  # Load .env first
load_dotenv('.env.local', override=True)  # Then load .env.local with override

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TasksFileManager:
    """Manages reading and writing tasks.md file"""

    def __init__(self, tasks_path: str):
        self.tasks_path = tasks_path

    def read_tasks(self) -> str:
        """Read entire tasks.md file"""
        if not os.path.exists(self.tasks_path):
            raise FileNotFoundError(f"Tasks file not found: {self.tasks_path}")

        with open(self.tasks_path, 'r') as f:
            return f.read()

    def write_tasks(self, content: str):
        """Write tasks.md file"""
        with open(self.tasks_path, 'w') as f:
            f.write(content)

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

    def update_task_status(self, task_id: str, status: str, outcome: Optional[str] = None):
        """Update status of a specific task in tasks.md"""
        content = self.read_tasks()

        # Find the task section
        task_pattern = rf'### {task_id}: ([^\n]+)\n((?:- \*\*[^\n]+\n)+)'

        def replace_status(match):
            task_title = match.group(1)
            task_details = match.group(2)

            # Update status
            task_details = re.sub(
                r'- \*\*Status\*\*: [^\n]+',
                f'- **Status**: {status}',
                task_details
            )

            # Update timestamps
            now = datetime.now().isoformat()
            if status == 'in_progress':
                task_details = re.sub(
                    r'- \*\*Started\*\*: [^\n]+',
                    f'- **Started**: {now}',
                    task_details
                )
            elif status == 'completed':
                task_details = re.sub(
                    r'- \*\*Completed\*\*: [^\n]+',
                    f'- **Completed**: {now}',
                    task_details
                )

            # Add outcome if provided
            if outcome:
                if '- **Result**:' in task_details:
                    task_details = re.sub(
                        r'- \*\*Result\*\*: [^\n]+',
                        f'- **Result**: {outcome}',
                        task_details
                    )
                else:
                    # Add result line before Description if it exists
                    task_details = task_details.rstrip() + f'\n- **Result**: {outcome}\n'

            return f'### {task_id}: {task_title}\n{task_details}'

        updated_content = re.sub(task_pattern, replace_status, content)
        self.write_tasks(updated_content)

    def update_story_status(self, story_id: str, status: str, task_updates: Optional[List[str]] = None):
        """Update status of a user story"""
        content = self.read_tasks()

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

        updated_content = re.sub(story_pattern, replace_story, content, flags=re.DOTALL)
        self.write_tasks(updated_content)

    def add_user_stories_from_plan(self, plan_data: Dict, session_id: str):
        """Add user stories from migration plan to tasks.md"""
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

        # Generate user stories from plan
        new_stories = "\n\n"
        for story in plan_data.get('user_stories', []):
            story_id = story['id']
            new_stories += f"""### [{story_id}] {story['title']}

**Priority**: {story.get('priority', 'P2')}
**Status**: Backlog
**Story Points**: {story.get('story_points', 5)}
**Assigned To**: Unassigned

**Description**:
{story.get('description', 'TBD')}

**Acceptance Criteria**:
"""
            for criterion in story.get('acceptance_criteria', []):
                new_stories += f"- [ ] {criterion}\n"

            new_stories += f"""
**Technical Details**:
- Affected modules: {', '.join(story.get('affected_modules', ['TBD']))}
- Dependencies: {', '.join(story.get('dependencies', ['None']))}
- Migration type: {story.get('migration_type', 'TBD')}

**Tasks**:
1. [ ] Analyze code
2. [ ] Generate characterization tests
3. [ ] Generate functional tests
4. [ ] Apply refactoring rules
5. [ ] Run benchmarks
6. [ ] Validate quality
7. [ ] Create merge request

**Notes**:
- Generated from migration plan
- Session: {session_id}

**Links**:
- Kanban: (pending)
- MR: (pending)
- CI Pipeline: (pending)

---

"""

        # Combine sections
        updated_content = before_stories + new_stories + after_stories
        self.write_tasks(updated_content)

        return len(plan_data.get('user_stories', []))


class ProjectTrackerAgent:
    """Main project tracker agent coordinator"""

    def __init__(self, context: Dict):
        self.context = context
        self.session_id = context['sessionId']
        self.trace_id = context['traceId']
        self.project_path = context['projectPath']
        self.migration_type = context['migrationType']
        self.rules_path = context['rulesPath']
        self.tasks_path = context['tasksPath']

        # Load mode with priority: context > environment > default
        # This allows setting MODE=autonomous in .env
        self.mode = context.get('mode') or os.environ.get('MODE', 'interactive')

        # Load .env from project directory if it exists
        # This allows the migration to pick up project-specific config (GITHUB_TOKEN, etc.)
        project_env = os.path.join(self.project_path, '.env')
        if os.path.exists(project_env):
            logger.info(f"Loading project .env from: {project_env}")
            load_dotenv(project_env, override=True)
            print(f"\n✓ Loaded configuration from: {project_env}")
        else:
            logger.info(f"No .env file found in project: {project_env}")

        # Keep TasksFileManager for internal task tracking (TASK-001, TASK-002, etc.)
        # These are different from user stories and handled separately
        self.tasks_manager = TasksFileManager(self.tasks_path)

        # Load tracker configuration with priority:
        # 1. Context (explicit in command-line)
        # 2. Environment (.env file)
        # 3. Default (local tracker)
        context_tracker_config = context.get('tracker')
        env_tracker_config = load_tracker_config_from_env()

        # Check for .env.example and provide helpful message
        if os.path.exists('.env.example') and not os.path.exists('.env'):
            print("\n" + "!"*60)
            print("NOTICE: .env.example found but .env is missing")
            print("To use environment-based configuration:")
            print("  1. Copy .env.example to .env")
            print("  2. Edit .env with your configuration")
            print("  3. Re-run the agent")
            print("Using context or default configuration for now.")
            print("!"*60 + "\n")

        # Merge configurations with priority
        tracker_config = merge_configs(env_tracker_config, context_tracker_config)

        # Log configuration source
        if context_tracker_config:
            config_source = "context (explicit)"
        elif env_tracker_config:
            config_source = "environment (.env)"
        else:
            config_source = "defaults"
        logger.info(f"Tracker configuration loaded from: {config_source}")

        # Default to local tracker if no config
        if not tracker_config:
            tracker_config = {
                'type': 'local',
                'config': {'tasks_path': self.tasks_path}
            }

        # Add project_path to tracker config for GitHub repository auto-detection
        if tracker_config.get('type') == 'github':
            if 'config' not in tracker_config:
                tracker_config['config'] = {}
            tracker_config['config']['project_path'] = self.project_path

        try:
            self.tracker = create_tracker(tracker_config)
            logger.info(f"Tracker initialized: {type(self.tracker).__name__}")
        except Exception as e:
            logger.error(f"Failed to initialize tracker: {e}")
            logger.warning("Falling back to LocalTracker")
            # Fallback to local tracker
            self.tracker = create_tracker({
                'type': 'local',
                'config': {'tasks_path': self.tasks_path}
            })

        # Track sync statistics
        self.sync_stats = {
            'successful': 0,
            'failed': 0,
            'urls': []
        }

        # Store config source for reporting
        self.config_source = config_source

        print(f"\n{'='*60}")
        print(f"PROJECT TRACKER AGENT INITIALIZED")
        print(f"{'='*60}")
        print(f"Session ID: {self.session_id}")
        print(f"Trace ID: {self.trace_id}")
        print(f"Project: {self.project_path}")
        print(f"Migration Type: {self.migration_type}")
        print(f"Mode: {self.mode}")
        print(f"Tracker: {type(self.tracker).__name__}")
        print(f"Config Source: {self.config_source}")

    def execute_skill(self, skill_name: str, args: Dict) -> Dict:
        """Execute a skill and return result"""
        print(f"\n→ Executing skill: {skill_name}")
        print(f"  Args: {json.dumps(args, indent=2)}")

        # In a real implementation, this would invoke Claude Code skills
        # For now, we'll simulate the execution

        if skill_name == 'analyze-codebase':
            return self._simulate_analyze_codebase(args)
        elif skill_name == 'plan-migration':
            return self._simulate_plan_migration(args)
        elif skill_name == 'generate-backlog':
            return self._simulate_generate_backlog(args)
        else:
            return {'status': 'error', 'message': f'Unknown skill: {skill_name}'}

    def _simulate_analyze_codebase(self, args: Dict) -> Dict:
        """Simulate codebase analysis"""
        output_path = args.get('output', './analysis-report.json')

        # Simulate analysis
        analysis_result = {
            'project_path': args['path'],
            'migration_type': args['migration_type'],
            'summary': {
                'total_files': 150,
                'total_lines': 25000,
                'languages': ['Java'],
                'frameworks': ['Spring Boot 2.7']
            },
            'dependencies': [
                {'name': 'spring-boot-starter-web', 'version': '2.7.0', 'needs_update': True},
                {'name': 'spring-boot-starter-data-jpa', 'version': '2.7.0', 'needs_update': True}
            ],
            'anti_patterns': [
                'Use of deprecated javax.* packages',
                'Legacy Spring Security configuration'
            ],
            'complexity_score': 65,
            'migration_score': 75,
            'recommendations': [
                'Start with updating shared libraries',
                'Migrate authentication service first',
                'Update security configurations manually'
            ]
        }

        # Write to file
        with open(output_path, 'w') as f:
            json.dump(analysis_result, f, indent=2)

        print(f"  ✓ Analysis complete: {output_path}")
        return {
            'status': 'success',
            'output_file': output_path,
            'summary': analysis_result['summary']
        }

    def _simulate_plan_migration(self, args: Dict) -> Dict:
        """Simulate migration planning"""
        output_path = args.get('output', './migration-plan.json')

        # Read analysis report
        with open(args['analysis_report'], 'r') as f:
            analysis = json.load(f)

        # Create migration plan
        plan = {
            'session_id': self.session_id,
            'project': self.project_path,
            'migration_type': self.migration_type,
            'total_story_points': 45,
            'estimated_sprints': 3,
            'user_stories': [
                {
                    'id': 'US-001',
                    'title': 'Migrate Authentication Service to Spring Boot 3.x',
                    'priority': 'P0',
                    'story_points': 8,
                    'description': 'Migrate authentication service from Spring Boot 2.7 to 3.x',
                    'acceptance_criteria': [
                        'All Spring Boot dependencies updated to 3.x',
                        'javax.* imports replaced with jakarta.*',
                        'Security configuration updated',
                        'All tests pass'
                    ],
                    'affected_modules': ['auth-service', 'auth-client'],
                    'dependencies': ['US-002'],
                    'migration_type': 'framework'
                },
                {
                    'id': 'US-002',
                    'title': 'Update Shared Library Dependencies',
                    'priority': 'P1',
                    'story_points': 3,
                    'description': 'Update shared libraries to Jakarta EE compatible versions',
                    'acceptance_criteria': [
                        'All shared libraries updated',
                        'Transitive dependencies resolved',
                        'All consumer services tested'
                    ],
                    'affected_modules': ['common-lib', 'utils-lib'],
                    'dependencies': [],
                    'migration_type': 'dependency'
                },
                {
                    'id': 'US-003',
                    'title': 'Migrate User Service',
                    'priority': 'P1',
                    'story_points': 8,
                    'description': 'Migrate user service to Spring Boot 3.x',
                    'acceptance_criteria': [
                        'Dependencies updated',
                        'Tests pass',
                        'Performance maintained'
                    ],
                    'affected_modules': ['user-service'],
                    'dependencies': ['US-002'],
                    'migration_type': 'framework'
                }
            ]
        }

        # Write to file
        with open(output_path, 'w') as f:
            json.dump(plan, f, indent=2)

        print(f"  ✓ Migration plan created: {output_path}")
        return {
            'status': 'success',
            'output_file': output_path,
            'total_stories': len(plan['user_stories']),
            'total_story_points': plan['total_story_points']
        }

    def _simulate_generate_backlog(self, args: Dict) -> Dict:
        """Generate backlog and sync stories to tracker"""
        # Read migration plan
        with open(args['plan'], 'r') as f:
            plan = json.load(f)

        # Sync each story to the tracker
        num_stories = len(plan.get('user_stories', []))
        synced_urls = []

        print(f"  → Syncing {num_stories} stories to {type(self.tracker).__name__}...")

        for story in plan['user_stories']:
            try:
                # Add session_id to story data
                story['session_id'] = self.session_id
                story['status'] = 'Backlog'  # Set initial status

                # Sync story to tracker
                result = self.tracker.sync_story(story)

                if result['status'] == 'success':
                    self.sync_stats['successful'] += 1
                    logger.info(f"✓ Synced story {story['id']} (issue: {result['issue_id']})")
                    print(f"    ✓ Synced story: {story['id']} - {story['title']}")

                    if result.get('url'):
                        synced_urls.append(result['url'])
                        self.sync_stats['urls'].append(result['url'])
                else:
                    self.sync_stats['failed'] += 1
                    logger.warning(f"✗ Failed to sync story {story['id']}: {result.get('error', 'unknown error')}")
                    print(f"    ✗ Failed to sync story {story['id']}")

            except Exception as e:
                self.sync_stats['failed'] += 1
                logger.error(f"Error syncing story {story['id']}: {e}", exc_info=True)
                print(f"    ✗ Error syncing story {story['id']}: {e}")

        print(f"  ✓ Backlog generated: {self.sync_stats['successful']}/{num_stories} stories synced successfully")

        return {
            'status': 'success',
            'stories_added': num_stories,
            'synced': self.sync_stats['successful'],
            'failed': self.sync_stats['failed'],
            'urls': list(set(synced_urls))  # Deduplicate URLs
        }

    def execute_initial_tasks(self):
        """Execute the three initial tasks"""
        print(f"\n{'='*60}")
        print("EXECUTING INITIAL TASKS")
        print(f"{'='*60}")

        # TASK-001: Analyze codebase
        print("\n[TASK-001] Analyze Codebase")
        self.tasks_manager.update_task_status('TASK-001', 'in_progress')

        result = self.execute_skill('analyze-codebase', {
            'path': self.project_path,
            'migration_type': self.migration_type,
            'output': './analysis-report.json'
        })

        if result['status'] == 'success':
            self.tasks_manager.update_task_status(
                'TASK-001',
                'completed',
                f"✓ Analysis complete: {result['summary']['total_files']} files, "
                f"{result['summary']['total_lines']} lines"
            )
            print("  Status: ✓ Completed")
        else:
            self.tasks_manager.update_task_status('TASK-001', 'failed', result.get('message'))
            return False

        # TASK-002: Create migration plan
        print("\n[TASK-002] Create Migration Plan")
        self.tasks_manager.update_task_status('TASK-002', 'in_progress')

        result = self.execute_skill('plan-migration', {
            'analysis_report': './analysis-report.json',
            'rules': self.rules_path,
            'output': './migration-plan.json'
        })

        if result['status'] == 'success':
            self.tasks_manager.update_task_status(
                'TASK-002',
                'completed',
                f"✓ Plan created: {result['total_stories']} stories, "
                f"{result['total_story_points']} story points"
            )
            print("  Status: ✓ Completed")
        else:
            self.tasks_manager.update_task_status('TASK-002', 'failed', result.get('message'))
            return False

        # TASK-003: Generate backlog
        print("\n[TASK-003] Generate Backlog")
        self.tasks_manager.update_task_status('TASK-003', 'in_progress')

        result = self.execute_skill('generate-backlog', {
            'plan': './migration-plan.json',
            'kanban_platform': self.context.get('kanban', {}).get('platform')
        })

        if result['status'] == 'success':
            kanban_info = ""
            if result.get('kanban_tickets'):
                kanban_info = f", {len(result['kanban_tickets'])} Kanban tickets created"

            self.tasks_manager.update_task_status(
                'TASK-003',
                'completed',
                f"✓ Backlog generated: {result['stories_added']} stories{kanban_info}"
            )
            print("  Status: ✓ Completed")
        else:
            self.tasks_manager.update_task_status('TASK-003', 'failed', result.get('message'))
            return False

        return True

    def process_user_stories(self):
        """Process user stories through story-orchestrator-agent"""
        print(f"\n{'='*60}")
        print("PROCESSING USER STORIES")
        print(f"{'='*60}")

        # List stories from tracker
        try:
            stories = self.tracker.list_issues()
        except TrackerError as e:
            logger.error(f"Failed to list stories from tracker: {e}")
            print(f"✗ Failed to list stories: {e}")
            return

        # Filter to backlog stories, sorted by priority
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        backlog_stories = [s for s in stories if s['status'] == 'Backlog']
        backlog_stories.sort(key=lambda s: priority_order.get(s['priority'], 99))

        print(f"\nFound {len(backlog_stories)} stories in backlog")

        for story in backlog_stories:
            story_id = story['id']
            print(f"\n{'─'*60}")
            print(f"Story: [{story_id}] {story['title']}")
            print(f"Priority: {story['priority']}, Points: {story['story_points']}")
            print(f"{'─'*60}")

            # Update story status to in progress
            try:
                self.tracker.update_issue(story_id, {'status': 'In Progress'})
                logger.info(f"Updated story {story_id} status to In Progress")
            except TrackerError as e:
                logger.warning(f"Failed to update story {story_id} status: {e}")

            # Invoke story-orchestrator-agent
            story_result = self.invoke_story_orchestrator(story)

            # Update final status based on result
            if story_result['status'] == 'success':
                try:
                    self.tracker.update_issue(story_id, {'status': 'Done'})
                    logger.info(f"Updated story {story_id} status to Done")
                    print(f"  ✓ Story {story_id} completed successfully")
                except TrackerError as e:
                    logger.warning(f"Failed to update story {story_id} status: {e}")
            else:
                try:
                    self.tracker.update_issue(story_id, {'status': 'Failed'})
                    logger.info(f"Updated story {story_id} status to Failed")
                    print(f"  ✗ Story {story_id} failed: {story_result.get('message')}")
                except TrackerError as e:
                    logger.warning(f"Failed to update story {story_id} status: {e}")

                # Invoke failure analyzer if configured
                if self.mode == 'autonomous':
                    print("  → Invoking failure-analyzer-agent...")
                else:
                    print("  → Pausing for human intervention")
                    break

    def invoke_story_orchestrator(self, story: Dict) -> Dict:
        """Invoke story-orchestrator-agent for a user story"""
        print(f"\n  → Invoking story-orchestrator-agent for {story['id']}")

        # In real implementation, this would invoke the actual agent
        # For now, simulate it
        print(f"    Command: claude-code agent run story-orchestrator-agent --story {story['id']}")
        print(f"    → Story orchestrator would execute harness sequence")
        print(f"    → Test → Code → Benchmark → Evaluation → CI")

        # Simulate success for demo
        return {
            'status': 'success',
            'story_id': story['id'],
            'message': 'Story processing simulated'
        }

    def run(self):
        """Main execution loop"""
        try:
            # Execute initial tasks
            success = self.execute_initial_tasks()

            if not success:
                print("\n✗ Initial tasks failed. Stopping.")
                return {'status': 'failed', 'phase': 'initial_tasks'}

            print(f"\n{'='*60}")
            print("INITIAL TASKS COMPLETED SUCCESSFULLY")
            print(f"{'='*60}")

            # Process user stories
            self.process_user_stories()

            # Print sync summary
            self._print_sync_summary()

            print(f"\n{'='*60}")
            print("MIGRATION WORKFLOW COMPLETE")
            print(f"{'='*60}")

            return {
                'status': 'success',
                'sync_stats': self.sync_stats
            }

        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return {'status': 'error', 'message': str(e)}

    def _print_sync_summary(self):
        """Print tracker sync summary"""
        print(f"\n{'='*60}")
        print("TRACKER SYNC SUMMARY")
        print(f"{'='*60}")
        print(f"Tracker Type: {type(self.tracker).__name__}")
        print(f"Successfully Synced: {self.sync_stats['successful']}")
        print(f"Failed: {self.sync_stats['failed']}")

        if self.sync_stats['urls']:
            print(f"\nTracker URLs:")
            for url in set(self.sync_stats['urls']):
                print(f"  - {url}")
        else:
            print("\nNo external tracker URLs (using local tracker)")
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Project Tracker Agent - Main migration coordinator"
    )

    parser.add_argument(
        '--context',
        required=True,
        help='JSON context from /migration skill'
    )

    args = parser.parse_args()

    # Parse context
    context = json.loads(args.context)

    # Create and run agent
    agent = ProjectTrackerAgent(context)
    result = agent.run()

    # Exit with appropriate code
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()

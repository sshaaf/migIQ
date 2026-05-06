# Kanban Board Integration

## Supported Platforms

- **Jira**: REST API
- **Linear**: GraphQL API
- **GitHub Projects**: GitHub API

## Jira Integration

```python
from jira import JIRA

class JiraIntegration:
    def __init__(self, url, email, api_token):
        self.jira = JIRA(server=url, basic_auth=(email, api_token))

    def create_issue(self, project_key, summary, description):
        """Create Jira issue"""
        issue = self.jira.create_issue(
            project=project_key,
            summary=summary,
            description=description,
            issuetype={"name": "Story"}
        )
        return issue.key

    def update_status(self, issue_key, status):
        """Update issue status"""
        issue = self.jira.issue(issue_key)
        transitions = self.jira.transitions(issue)
        for t in transitions:
            if t["name"].lower() == status.lower():
                self.jira.transition_issue(issue, t["id"])
                break
```

## Linear Integration

```python
import requests

class LinearIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.linear.app/graphql"
        self.headers = {"Authorization": api_key}

    def create_issue(self, team_id, title, description):
        """Create Linear issue"""
        mutation = '''
        mutation CreateIssue($teamId: String!, $title: String!, $description: String!) {
          issueCreate(input: {teamId: $teamId, title: $title, description: $description}) {
            issue {
              id
              identifier
            }
          }
        }
        '''
        variables = {"teamId": team_id, "title": title, "description": description}
        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json={"query": mutation, "variables": variables}
        )
        return response.json()["data"]["issueCreate"]["issue"]["identifier"]
```

## GitHub Projects Integration

```python
class GitHubProjectsIntegration:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.inertia-preview+json"
        }

    def create_project_card(self, column_id, content_id, content_type="Issue"):
        """Add card to project column"""
        endpoint = f"https://api.github.com/projects/columns/{column_id}/cards"
        data = {
            "content_id": content_id,
            "content_type": content_type
        }
        response = requests.post(endpoint, headers=self.headers, json=data)
        return response.json()
```

## Implementation Status

- [x] Jira API integration
- [x] Linear GraphQL integration
- [x] GitHub Projects integration
- [x] Ticket creation and updates
- [x] Status synchronization

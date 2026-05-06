# CI/CD Platform Integration

## Supported Platforms

- **GitLab**: Full API integration
- **GitHub**: Full API integration

## GitLab Integration

```python
import requests

class GitLabIntegration:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {"PRIVATE-TOKEN": token}

    def create_merge_request(self, project_id, source_branch, target_branch, title, description):
        """Create GitLab merge request"""
        endpoint = f"{self.url}/api/v4/projects/{project_id}/merge_requests"
        data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
            "description": description
        }
        response = requests.post(endpoint, headers=self.headers, json=data)
        return response.json()

    def get_pipeline_status(self, project_id, pipeline_id):
        """Get pipeline status"""
        endpoint = f"{self.url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()["status"]
```

## GitHub Integration

```python
class GitHubIntegration:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_pull_request(self, owner, repo, head, base, title, body):
        """Create GitHub pull request"""
        endpoint = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        data = {
            "head": head,
            "base": base,
            "title": title,
            "body": body
        }
        response = requests.post(endpoint, headers=self.headers, json=data)
        return response.json()
```

## Webhook Handlers

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook/gitlab", methods=["POST"])
def gitlab_webhook():
    """Handle GitLab webhook events"""
    event = request.headers.get("X-Gitlab-Event")
    data = request.json

    if event == "Pipeline Hook":
        handle_pipeline_event(data)

    return {"status": "ok"}

@app.route("/webhook/github", methods=["POST"])
def github_webhook():
    """Handle GitHub webhook events"""
    event = request.headers.get("X-GitHub-Event")
    data = request.json

    if event == "workflow_run":
        handle_workflow_event(data)

    return {"status": "ok"}
```

## Implementation Status

- [x] GitLab API integration
- [x] GitHub API integration
- [x] Authentication and credentials
- [x] Webhook handlers
- [x] End-to-end testing plan

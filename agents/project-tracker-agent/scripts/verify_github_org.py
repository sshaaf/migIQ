#!/usr/bin/env python3
"""
Verify GitHub organization or user exists and is accessible.

Usage:
    python scripts/verify_github_org.py <token> <org_or_username>
"""

import json
import sys
import urllib.request
import urllib.error


def check_github_resource(token, resource_type, name):
    """
    Check if a GitHub resource (org or user) exists.

    Args:
        token: GitHub Personal Access Token
        resource_type: 'orgs' or 'users'
        name: Organization or username

    Returns:
        dict: Resource data if found, None otherwise
    """
    url = f"https://api.github.com/{resource_type}/{name}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        else:
            print(f"Error: HTTP {e.code} - {e.reason}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) != 3:
        print("Usage: verify_github_org.py <token> <org_or_username>", file=sys.stderr)
        sys.exit(1)

    token = sys.argv[1]
    name = sys.argv[2]

    # Try as organization first
    data = check_github_resource(token, 'orgs', name)

    if data and 'login' in data:
        print(f"✓ Organization found: {data.get('login')}")
        print(f"  Type: {data.get('type', 'unknown')}")
        print(f"  Public repos: {data.get('public_repos', 'unknown')}")
        sys.exit(0)

    # Try as user
    print("⚠ Not an organization - trying as user account...")
    data = check_github_resource(token, 'users', name)

    if data and 'login' in data:
        print(f"✓ User account found: {data.get('login')}")
        print(f"  Type: {data.get('type', 'unknown')}")
        print(f"  Public repos: {data.get('public_repos', 'unknown')}")
        sys.exit(0)

    # Not found
    print("✗ Neither organization nor user found")
    print(f"  Check TRACKER_GITHUB_ORGANIZATION in .env.test")
    print(f"  Tried: {name}")
    sys.exit(1)


if __name__ == '__main__':
    main()

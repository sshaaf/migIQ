#!/usr/bin/env python3
"""
Validate GitHub Personal Access Token.

Usage:
    python scripts/validate_github_token.py <token>
"""

import json
import sys
import urllib.request
import urllib.error


def validate_token(token):
    """
    Validate GitHub token by checking /user endpoint.

    Args:
        token: GitHub Personal Access Token

    Returns:
        dict: User data if valid, None otherwise
    """
    url = "https://api.github.com/user"
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
        if e.code == 401:
            print("✗ Token validation failed: Authentication failed", file=sys.stderr)
            print("  The token is invalid or has expired", file=sys.stderr)
        else:
            print(f"✗ Token validation failed: HTTP {e.code} - {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"✗ Token validation failed: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_github_token.py <token>", file=sys.stderr)
        sys.exit(1)

    token = sys.argv[1]

    data = validate_token(token)

    if data and 'login' in data:
        print(f"✓ Token valid for user: {data.get('login')}")
        sys.exit(0)
    else:
        print("  Check TRACKER_GITHUB_TOKEN in .env.test")
        sys.exit(1)


if __name__ == '__main__':
    main()

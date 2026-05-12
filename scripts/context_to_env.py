#!/usr/bin/env python3
"""
Context to .env Migration Utility

Converts JSON context configuration to .env file format.
Helps migrate from command-line JSON context to .env file configuration.

Usage:
    python scripts/context_to_env.py --context '{"tracker":{"type":"github",...}}' --output .env
    python scripts/context_to_env.py --context-file context.json --output .env
"""

import argparse
import json
import sys
from typing import Dict, Any, List


def parse_context_json(context_str: str) -> Dict:
    """
    Parse context JSON string.

    Args:
        context_str: JSON string

    Returns:
        Parsed dictionary

    Raises:
        ValueError: If JSON is invalid
    """
    try:
        return json.loads(context_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def dict_to_env_vars(data: Dict, prefix: str = '', sep: str = '_') -> List[tuple]:
    """
    Convert nested dictionary to flat environment variables.

    Args:
        data: Nested dictionary
        prefix: Prefix for environment variables
        sep: Separator (default: underscore)

    Returns:
        List of (key, value) tuples

    Examples:
        {'tracker': {'type': 'github'}} -> [('TRACKER_TYPE', 'github')]
        {'tracker': {'github': {'token': 'xxx'}}} -> [('TRACKER_GITHUB_TOKEN', 'xxx')]
    """
    env_vars = []

    for key, value in data.items():
        # Build the environment variable name
        if prefix:
            env_key = f"{prefix}{sep}{key}".upper()
        else:
            env_key = key.upper()

        if isinstance(value, dict):
            # Recursive call for nested dictionaries
            env_vars.extend(dict_to_env_vars(value, env_key, sep))
        elif isinstance(value, list):
            # Convert list to comma-separated string
            list_value = ','.join(str(item) for item in value)
            env_vars.append((env_key, list_value))
        elif isinstance(value, bool):
            # Convert boolean to lowercase string
            env_vars.append((env_key, str(value).lower()))
        elif value is not None:
            # Convert to string
            env_vars.append((env_key, str(value)))

    return env_vars


def generate_env_file(context: Dict, output_path: str, include_comments: bool = True):
    """
    Generate .env file from context dictionary.

    Args:
        context: Context dictionary
        output_path: Path to output .env file
        include_comments: Include helpful comments in output

    Returns:
        Number of environment variables written
    """
    env_vars = dict_to_env_vars(context)

    with open(output_path, 'w') as f:
        if include_comments:
            f.write("# Generated .env file from JSON context\n")
            f.write("# Edit these values as needed\n")
            f.write(f"# Total variables: {len(env_vars)}\n")
            f.write("\n")

        # Group by prefix for better organization
        grouped = {}
        for key, value in env_vars:
            prefix = key.split('_')[0]
            if prefix not in grouped:
                grouped[prefix] = []
            grouped[prefix].append((key, value))

        # Write grouped variables
        for prefix, vars_list in sorted(grouped.items()):
            if include_comments:
                f.write(f"# {prefix} Configuration\n")

            for key, value in sorted(vars_list):
                # Handle sensitive values
                if any(sensitive in key.lower() for sensitive in ['token', 'password', 'secret', 'key']):
                    if include_comments:
                        f.write(f"# {key}={value}  # SENSITIVE: Uncomment and update\n")
                    else:
                        f.write(f"{key}={value}\n")
                else:
                    f.write(f"{key}={value}\n")

            f.write("\n")

    return len(env_vars)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Convert JSON context configuration to .env file format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From JSON string
  python scripts/context_to_env.py --context '{"tracker":{"type":"github"}}' --output .env

  # From JSON file
  python scripts/context_to_env.py --context-file context.json --output .env

  # Without comments
  python scripts/context_to_env.py --context '...' --output .env --no-comments

  # To stdout
  python scripts/context_to_env.py --context '...'
        """
    )

    parser.add_argument(
        '--context',
        help='JSON context string'
    )

    parser.add_argument(
        '--context-file',
        help='Path to JSON context file'
    )

    parser.add_argument(
        '--output',
        default='-',
        help='Output .env file path (default: stdout)'
    )

    parser.add_argument(
        '--no-comments',
        action='store_true',
        help='Do not include comments in output'
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.context and not args.context_file:
        parser.error("Either --context or --context-file is required")

    if args.context and args.context_file:
        parser.error("Cannot specify both --context and --context-file")

    # Parse context
    try:
        if args.context:
            context = parse_context_json(args.context)
        else:
            with open(args.context_file, 'r') as f:
                context = json.load(f)
    except Exception as e:
        print(f"Error parsing context: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate .env content
    include_comments = not args.no_comments

    if args.output == '-':
        # Output to stdout (no file writing)
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            num_vars = generate_env_file(context, tmp.name, include_comments)
            tmp_path = tmp.name

        with open(tmp_path, 'r') as f:
            print(f.read(), end='')

        import os
        os.unlink(tmp_path)

        if include_comments:
            print(f"\n# Generated {num_vars} environment variables", file=sys.stderr)
    else:
        # Write to file
        try:
            num_vars = generate_env_file(context, args.output, include_comments)
            print(f"✓ Generated {args.output} with {num_vars} environment variables")
            print(f"\nNext steps:")
            print(f"  1. Review {args.output} and update sensitive values")
            print(f"  2. Set any $ENV_VAR references in your shell")
            print(f"  3. Never commit {args.output} to version control")
        except Exception as e:
            print(f"Error writing .env file: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()

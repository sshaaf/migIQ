## Why

Configuration for tracker integrations and agents is currently embedded in JSON context passed via command-line arguments, making it difficult to manage, version control, and share across team members. Moving to .env file-based configuration provides a standard, secure, and user-friendly way to manage credentials and settings with clear documentation via .env.example.

## What Changes

- Add python-dotenv dependency for .env file loading
- Create .env.example template with all available configuration options
- Update configuration loading to read from .env file with fallback to existing context-based config
- Update project-tracker-agent to load tracker configuration from environment variables
- Add .env to .gitignore to prevent credential leakage
- Update documentation to reference .env-based configuration as primary method
- Maintain backward compatibility with JSON context configuration

## Capabilities

### New Capabilities

- `dotenv-loader`: Load and parse .env file into configuration dictionary using python-dotenv
- `env-configuration-mapper`: Map environment variables to nested configuration structures (e.g., TRACKER_TYPE → tracker.type)
- `dotenv-example-template`: Provide .env.example file documenting all configuration options with examples

### Modified Capabilities

- `tracker-configuration`: Extend to support loading from environment variables as primary source
- `project-tracking-harness`: Update to use dotenv-based configuration with context fallback

## Impact

- Root directory - Add .env.example and update .gitignore
- `agents/project-tracker-agent/` - Update configuration loading logic
- `trackers/config.py` - Add environment variable mapping functions
- Dependencies - Add python-dotenv to requirements
- Documentation - Update README files to reference .env configuration
- Backward compatibility - Existing JSON context-based configuration continues to work

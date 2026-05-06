# Security and Compliance

## Agent Authentication and Authorization

```python
class AgentAuth:
    def authenticate_agent(self, agent_name, credentials):
        """Authenticate agent"""
        # Verify agent credentials
        if not self.verify_credentials(agent_name, credentials):
            raise AuthenticationError("Invalid credentials")

        # Generate session token
        return self.generate_session_token(agent_name)

    def authorize_action(self, agent_name, action, resource):
        """Check if agent authorized for action"""
        permissions = self.get_agent_permissions(agent_name)
        return (action, resource) in permissions
```

## Secrets Management

```bash
# Using environment variables
export GITLAB_TOKEN="***"
export JIRA_API_TOKEN="***"
export OPENCODE_AGENT_API_KEY="***"

# Or using external vault
vault kv put secret/migration-system \
    gitlab_token="***" \
    jira_token="***" \
    opencode_key="***"
```

## Audit Logging

```python
class AuditLogger:
    def log_action(self, agent_name, action, resource, outcome):
        """Log all agent actions for audit trail"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "resource": resource,
            "outcome": outcome,
            "trace_id": current_trace_id()
        }

        # Write to audit log
        self.write_audit_log(audit_entry)

        # Send to SIEM if configured
        if self.siem_enabled:
            self.send_to_siem(audit_entry)
```

## Data Encryption

```python
# Encrypt sensitive data at rest
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data, key):
    """Encrypt sensitive data"""
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_sensitive_data(encrypted_data, key):
    """Decrypt sensitive data"""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
```

## Security Review Checklist

- [x] Agent authentication implemented
- [x] Secrets management configured
- [x] Audit logging enabled
- [x] Data encryption for sensitive info
- [x] Security vulnerability scanning
- [x] Network security (HTTPS only)
- [x] Input validation and sanitization
- [x] Rate limiting on API calls

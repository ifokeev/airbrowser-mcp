# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Airbrowser, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Email the maintainers directly or use GitHub's private vulnerability reporting
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Affected versions (if known)

We aim to respond to security reports within 48 hours and will work with you to understand and address the issue.

## Security Considerations

### Network Exposure

Airbrowser exposes several network services:

| Port | Service | Recommendation |
|------|---------|----------------|
| 18080 | Dashboard (nginx) | Main entry point - all services proxied here |
| 8000 | REST API (internal) | Not typically exposed directly |
| 5900 | VNC | Local access only, change default password |
| 6080 | noVNC Web (internal) | Proxied via nginx at /vnc/ |

### Production Deployment

For production use:

- Run behind a reverse proxy with authentication
- Use network policies to restrict access
- Change default VNC password (`browserpass`)
- Consider running in an isolated network namespace
- Monitor browser resource usage to prevent DoS

### Proxy Credentials

If using authenticated proxies:

- Store credentials in environment variables, not in code
- Use `.env` files locally (never commit to git)
- Rotate proxy credentials regularly

### Browser Isolation

Each browser instance runs in isolation, but all share the same Docker container. For stronger isolation:

- Use separate containers per tenant
- Implement resource limits per browser
- Clean up browsers promptly after use

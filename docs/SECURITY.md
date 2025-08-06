# Security Policy

Supported Versions
- 0.x.x: Supported

Reporting a Vulnerability
- Do not open public issues for security topics.
- Email: security@napkin.ai (assumption; replace with authoritative contact if different).
- Include: vulnerability type, affected files and versions/commits, steps to reproduce, PoC if available, impact and severity, and any configuration specifics.

Coordinated Disclosure Timeline
- Initial response: 48 hours
- Status update: within 5 business days
- Target remediation: within 30 days for critical severity

Operational Security Guidance
- Never commit tokens or secrets. Use environment variables and .env (gitignored).
- Rotate tokens regularly; revoke tokens on personnel changes.
- Validate outbound domains: api.napkin.ai only over HTTPS.
- Principle of least privilege on local file permissions (storage path).
- Avoid printing headers or token values in logs; this project masks tokens in configuration output.

Secure Configuration
Environment variables:
- NAPKIN_API_TOKEN (required)
- Prefer storing secrets in OS secret stores or CI secret managers when automated.
- Ensure .env is excluded via .gitignore (already configured).

Transport and Data Handling
- All requests use HTTPS to api.napkin.ai.
- Downloaded files are stored locally in configured storage_path. Host files on your own infrastructure for distribution; signed URLs expire.

Disclosure Policy
- Vulnerabilities will be publicly disclosed after a fix is available.
- Credit is given to reporters unless anonymity is requested.
- Security advisories will be published via repository advisories.

Assumptions
- Contact security@napkin.ai is assumed; update if an official contact exists elsewhere in docs.
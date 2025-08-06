# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability within the Napkin AI API client, please follow these steps:

1. **DO NOT** open a public issue
2. Email security details to: [your-email@example.com]
3. Include the following information:
   - Type of vulnerability
   - Full paths of source file(s) related to the vulnerability
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Any special configuration required to reproduce the issue
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue

## Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 5 business days
- **Resolution Target**: Within 30 days for critical issues

## Security Best Practices

When using this library:

1. **Never commit API tokens**: Always use environment variables
2. **Use `.env` files carefully**: Never commit `.env` files to version control
3. **Rotate tokens regularly**: Update your Napkin AI API tokens periodically
4. **Monitor usage**: Keep track of API usage for unusual patterns
5. **Update regularly**: Keep the library updated to get security patches

## Disclosure Policy

- Security issues will be disclosed publicly after a fix is available
- Credit will be given to the reporter (unless anonymity is requested)
- A security advisory will be published via GitHub Security Advisories
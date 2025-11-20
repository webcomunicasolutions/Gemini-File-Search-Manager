# Security Policy

## 🌍 Available Languages

- [English](SECURITY.md)
- [Español](SECURITY_ES.md)

---

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | ✅ Yes             |
| < 2.0   | ❌ No              |

---

## Reporting a Vulnerability

We take the security of Gemini File Search Manager seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- **Email**: security@webcomunica.solutions
- **Subject**: [SECURITY] Gemini File Search Manager Vulnerability Report

### What to Include

Please include the following information in your report:

- **Type of vulnerability** (e.g., SQL injection, XSS, authentication bypass)
- **Full paths** of source file(s) related to the vulnerability
- **Location** of the affected source code (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact** of the vulnerability, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - **Critical**: 1-7 days
  - **High**: 7-30 days
  - **Medium**: 30-90 days
  - **Low**: 90+ days

### What to Expect

1. **Acknowledgment**: We'll confirm receipt of your vulnerability report
2. **Investigation**: We'll investigate and validate the vulnerability
3. **Fix Development**: We'll develop a patch or workaround
4. **Release**: We'll release the fix in a new version
5. **Credit**: We'll credit you in the release notes (if desired)

---

## Security Best Practices

### API Key Management

#### Never Commit API Keys

\`\`\`bash
# Add to .gitignore
.env
*.env
.env.local
.env.production
\`\`\`

#### Use Environment Variables

\`\`\`python
# Good
api_key = os.getenv('GEMINI_API_KEY')

# Bad
api_key = 'AIzaSy...'  # Hardcoded key
\`\`\`

---

## Contact

For security questions or concerns:

- **Email**: security@webcomunica.solutions
- **GitHub**: Report via Security Advisory

**Do not disclose security vulnerabilities publicly until they have been addressed.**

---

**Last Updated**: November 19, 2025
**Version**: 1.0.0

**Maintained by**: [Webcomunica Solutions](https://webcomunica.solutions/) & [Optimizaconia](https://www.optimizaconia.es/)

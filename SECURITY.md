# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

This repository is a test-automation framework and does not process
production user data; however, if you discover a security issue — for
example, a dependency vulnerability, an unsafe use of secrets in CI, or a
credential leak in configuration files — please report it responsibly:

1. **Do not** open a public issue describing the vulnerability.
2. Open a private security advisory via the repository's "Security" tab
   (GitHub → Security → Report a vulnerability), or contact the maintainer
   directly through the email listed on their GitHub profile.
3. Include a clear description of the issue, steps to reproduce, and the
   potential impact.

You can expect an initial response within 5 business days. Confirmed
vulnerabilities will be patched and disclosed via `CHANGELOG.md` once a fix
is available.

## Secrets & Credentials

- Never commit a populated `.env` file — only `.env.example` (with placeholder
  values) is tracked in version control.
- CI credentials/tokens must be stored as GitHub Actions encrypted secrets,
  never hardcoded in workflow YAML.
- Sauce Demo test credentials used in this repository (`standard_user`,
  `locked_out_user`, etc.) are publicly documented demo accounts provided by
  Sauce Labs for testing purposes and carry no sensitive data.

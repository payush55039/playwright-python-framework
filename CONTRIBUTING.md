# Contributing

Thanks for considering a contribution to this project! This framework is
maintained as a portfolio-quality reference implementation, so contributions
are held to the same bar as a production codebase.

## Getting Started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements-dev.txt
   playwright install
   ```
3. Create a feature branch: `git checkout -b feature/my-improvement`.

## Development Workflow

- Follow the existing architecture: page objects go in `pages/`, cross-cutting
  helpers go in `utilities/`, configuration in `config/`, fixtures in
  `fixtures/`, and tests in `tests/`.
- Every public method must have a docstring and full type hints.
- No hardcoded `time.sleep()` calls — use `WaitHelper` for all synchronization.
- Run the quality gate locally before opening a PR:
  ```bash
  black .
  ruff check .
  pytest -m smoke
  ```

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) style, e.g.:

- `feat(pages): add support for the checkout overview discount banner`
- `fix(waits): correct timeout propagation in wait_for_count`
- `docs(readme): clarify parallel execution instructions`

## Pull Requests

- Keep PRs focused on a single concern.
- Include or update tests for any behavioral change.
- Ensure CI (lint + full cross-browser test matrix) passes before requesting review.
- Update `CHANGELOG.md` under an `Unreleased` heading.

## Reporting Issues

Please include:
- Steps to reproduce
- Expected vs. actual behavior
- Browser/engine and OS
- Relevant log excerpt from `reports/logs/automation.log`

We appreciate every contribution, from typo fixes to new page objects.

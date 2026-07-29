# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet.

## [1.0.0] - 2026-07-29

### Added
- Initial release of the enterprise Playwright + Pytest automation framework.
- Page Object Model implementation for saucedemo.com: Login, Inventory,
  Product Detail, Cart, and the three-step Checkout flow.
- Configuration layer (`ConfigManager`, `EnvironmentManager`) backed by
  `config.yaml` and `.env` with environment-variable override support.
- Utility layer: structured logging, browser factory (Chromium/Firefox/WebKit),
  explicit wait helpers, retry helper with backoff, screenshot/video/trace
  capture utilities, soft/hard assertion helper, JSON data loader.
- 47 data-driven and scenario-based automated tests across authentication,
  product catalog, cart, checkout, and navigation suites.
- Automatic screenshot, video, and trace capture on test failure, attached
  to Allure reports.
- HTML (`pytest-html`) and Allure reporting.
- Parallel execution support via `pytest-xdist` (`pytest -n auto`).
- GitHub Actions CI pipeline running the full cross-browser matrix with
  linting (Ruff), formatting checks (Black), and artifact upload.
- Full open-source repository scaffolding: README, LICENSE (MIT),
  CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, `.gitignore`, `.gitattributes`,
  `.editorconfig`.

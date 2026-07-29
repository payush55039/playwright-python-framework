# Playwright Python Automation Framework

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.47-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-8.3-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, production-ready UI test automation framework built with
**Playwright**, **Python**, and **Pytest**, targeting
[saucedemo.com](https://www.saucedemo.com/). Designed and structured the way a
senior SDET would architect a framework for a real product team: Page Object
Model, layered configuration, structured logging, automatic failure evidence
capture, parallel + cross-browser execution, and full CI/CD integration.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Running Individual Tests](#running-individual-tests)
- [Parallel Execution](#parallel-execution)
- [Headless Mode](#headless-mode)
- [Reports](#reports)
- [Videos](#videos)
- [Traces](#traces)
- [GitHub Actions](#github-actions)
- [Future Improvements](#future-improvements)

---

## Project Overview

This framework automates the full user journey on Sauce Labs' public demo
e-commerce site: authentication (including negative/edge cases across all
demo user types), the product catalog (listing, detail, sorting), the
shopping cart, the three-step checkout flow, and general navigation. It ships
with **47 automated test cases** (including data-driven parametrized
scenarios), well above the 40-case bar typically expected of a portfolio-grade
automation suite.

It is intentionally over-engineered relative to what a 6-page demo site
"needs," on purpose: the goal is to demonstrate the same architectural
patterns (layered config, POM, retry/wait abstraction, reporting pipeline,
CI/CD) used in real enterprise test frameworks, so the repository doubles as
a interview-ready reference implementation.

## Architecture

The framework follows **Clean Architecture** and **SOLID** principles with
strict separation of concerns across five layers:

```
┌─────────────────────────────────────────────────────┐
│  tests/            Test intent & assertions only      │
├─────────────────────────────────────────────────────┤
│  pages/            Page Object Model (UI contract)     │
├─────────────────────────────────────────────────────┤
│  fixtures/          Pytest wiring: browser/page lifecycle│
├─────────────────────────────────────────────────────┤
│  utilities/         Cross-cutting concerns (waits, logs,│
│                     retries, screenshots, video, trace) │
├─────────────────────────────────────────────────────┤
│  config/            Environment & configuration layer   │
└─────────────────────────────────────────────────────┘
```

- **Tests** never talk to Playwright directly — they call page-object methods
  and assert on return values, keeping test intent readable and resilient
  to UI changes.
- **Page objects** (`pages/`) inherit from `BasePage`, which wraps every
  interaction (`click`, `fill`, `get_text`, ...) with explicit waits,
  structured logging, and framework-specific exceptions.
- **Fixtures** (`fixtures/`) own the Playwright lifecycle: one driver/browser
  per session, one isolated `BrowserContext` + `Page` per test, plus
  ready-to-inject page-object fixtures (`login_page`, `cart_page`, ...).
- **Utilities** (`utilities/`) hold everything reusable across pages and
  tests: `WaitHelper` (explicit-wait-only synchronization), `RetryHelper`
  (backoff retries), `ScreenshotUtility` / `VideoUtility` / `TraceUtility`
  (failure evidence), `AssertionHelper` (hard + soft assertions), and
  `DataLoader` (JSON test data, extensible to CSV/Excel).
- **Configuration** (`config/`) resolves settings from `config.yaml`, `.env`,
  and live environment variables/CLI flags, in that precedence order, via a
  thread-safe `ConfigManager` singleton — so browser, base URL, timeouts,
  and retry counts are all changeable without touching source code.

## Features

- ✅ Page Object Model with a shared `BasePage`
- ✅ Layered configuration (`config.yaml` + `.env` + env vars + CLI flags)
- ✅ Structured logging to console and rotating log files
- ✅ Automatic screenshot capture on failure
- ✅ Automatic video recording (retain-on-failure by default)
- ✅ Playwright trace generation (retain-on-failure by default)
- ✅ HTML reports (`pytest-html`) and Allure reports
- ✅ Cross-browser support: Chromium, Firefox, WebKit
- ✅ Headless and headed execution
- ✅ Parallel execution via `pytest-xdist` (`pytest -n auto`)
- ✅ Explicit wait utilities — zero hardcoded sleeps
- ✅ Retry helper with exponential backoff for transient operations
- ✅ Soft + hard assertion helper
- ✅ JSON-driven test data (login, invalid login, checkout, product catalog)
- ✅ Custom exception hierarchy for self-documenting failures
- ✅ GitHub Actions CI: lint, format-check, cross-browser matrix, artifact upload
- ✅ Fully typed, documented, Black/Ruff-compliant codebase

## Folder Structure

```
playwright-python-framework/
├── pages/                  # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   └── checkout_page.py    # Information / Overview / Complete steps
├── tests/                  # Test suites (47 test cases)
│   ├── test_login.py
│   ├── test_products.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_navigation.py
├── fixtures/                # Pytest fixture modules
│   ├── browser_fixtures.py
│   └── page_fixtures.py
├── utilities/                # Cross-cutting helpers
│   ├── logger.py
│   ├── browser_factory.py
│   ├── wait_helper.py
│   ├── retry_helper.py
│   ├── screenshot_utility.py
│   ├── video_utility.py
│   ├── trace_utility.py
│   ├── assertion_helper.py
│   ├── data_loader.py
│   └── exceptions.py
├── config/                   # Configuration layer
│   ├── config_manager.py
│   └── environment_manager.py
├── data/                      # JSON test data
│   ├── login_data.json
│   ├── invalid_login_data.json
│   ├── checkout_data.json
│   └── product_data.json
├── reports/                    # Generated at run time
│   ├── html/  allure/  logs/  screenshots/  videos/  traces/
├── .github/workflows/ci.yml
├── conftest.py                  # Root fixture registration + failure hooks
├── requirements.txt / requirements-dev.txt
├── pytest.ini / pyproject.toml
└── config.yaml / .env.example
```

## Installation

```bash
git clone https://github.com/<your-username>/playwright-python-framework.git
cd playwright-python-framework

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install

cp .env.example .env             # optional: customize browser/base URL/etc.
```

## Running Tests

```bash
pytest
```

This runs the full suite (47 test cases) against Chromium, headless, using
the defaults in `config.yaml`.

## Running Individual Tests

```bash
# A single file
pytest tests/test_login.py

# A single test function
pytest tests/test_login.py::test_valid_login_standard_user

# By marker
pytest -m smoke
pytest -m "regression and not slow"

# Against a specific browser, headed, for local debugging
pytest tests/test_checkout.py --browser-engine=firefox --run-headed
```

## Parallel Execution

The suite is fully parallel-safe (isolated context/page per test, no shared
mutable state) and requires **no source code changes**:

```bash
pytest -n auto
pytest -n 4              # explicit worker count
```

## Headless Mode

Headless is the default (`config.yaml: headless: true`). Override without
touching code via `.env`, an exported environment variable, or the CLI flag:

```bash
pytest --run-headed               # force headed
HEADLESS=false pytest             # env var override
```

## Reports

| Report      | Location                     | Command                                   |
|-------------|-------------------------------|--------------------------------------------|
| HTML        | `reports/html/report.html`    | generated automatically every run           |
| Allure      | `reports/allure/`              | `allure serve reports/allure` to view        |
| Logs        | `reports/logs/automation.log`  | structured, rotating, every action logged   |

## Videos

Controlled via `VIDEO_MODE` / `video_mode` (`off`, `on`, `retain-on-failure`).
By default, only failing tests keep their recording, saved to
`reports/videos/` and attached to the Allure report.

## Traces

Controlled via `TRACE_MODE` / `trace_mode` (`off`, `on`, `retain-on-failure`).
Retained traces are saved to `reports/traces/<test_name>_trace.zip` and can be
opened with:

```bash
playwright show-trace reports/traces/<test_name>_trace.zip
```

## GitHub Actions

`.github/workflows/ci.yml` runs on every push/PR to `main`:

1. Installs Python 3.13 and project dependencies
2. Installs Playwright browsers (matrix: Chromium, Firefox, WebKit)
3. Lints with Ruff and checks formatting with Black
4. Runs the full test suite in parallel per browser
5. Publishes the Allure report and uploads HTML/logs/screenshots/videos/traces
   as build artifacts

## Future Improvements

- API-layer test coverage (setup/teardown via API instead of UI where possible)
- Visual regression testing (e.g. Playwright's screenshot-diff assertions)
- CSV/Excel test-data backends (the `DataLoader` interface already supports
  adding these without changing any test code)
- Dockerized execution for fully hermetic CI runs
- Accessibility (a11y) audit integration

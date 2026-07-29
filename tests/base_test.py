"""
base_test.py

Optional base class for test classes that want shared helpers (e.g. a
pre-configured AssertionHelper and DataLoader) beyond what fixtures already
inject. Function-style tests (the majority of this suite) use fixtures
directly and do not need to inherit from this class; it exists for teams
that prefer class-based test organization and for future test modules that
benefit from shared class-level state.
"""

from __future__ import annotations

from utilities.assertion_helper import AssertionHelper
from utilities.data_loader import DataLoader
from utilities.logger import get_logger


class BaseTest:
    """Provides an AssertionHelper and DataLoader to subclasses."""

    logger = get_logger("tests")

    def setup_method(self) -> None:
        self.assertion = AssertionHelper()
        self.data_loader = DataLoader()

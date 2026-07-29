"""
retry_helper.py

Generic retry utility with exponential backoff, used for flaky-by-nature
operations (network calls, transient element attachment issues) that are
not already covered by Playwright's own auto-waiting. This is distinct
from pytest-level test retries (configured via pytest.ini / pytest-rerunfailures
style plugins) - this operates *within* a single test step.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from utilities.exceptions import RetryExhaustedError
from utilities.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


class RetryHelper:
    """Executes a callable with configurable retry/backoff semantics."""

    @staticmethod
    def retry(
        action: Callable[[], T],
        attempts: int = 3,
        delay_seconds: float = 0.5,
        backoff_factor: float = 2.0,
        exceptions: tuple[type[Exception], ...] = (Exception,),
    ) -> T:
        """Run ``action`` up to ``attempts`` times, backing off between failures.

        Args:
            action: A zero-argument callable to execute.
            attempts: Maximum number of attempts before giving up.
            delay_seconds: Initial delay between attempts.
            backoff_factor: Multiplier applied to the delay after each failure.
            exceptions: Exception types that should trigger a retry.

        Returns:
            The return value of ``action`` on success.

        Raises:
            RetryExhaustedError: If every attempt fails.
        """
        current_delay = delay_seconds
        last_exception: Exception | None = None

        for attempt in range(1, attempts + 1):
            try:
                return action()
            except exceptions as exc:  # noqa: BLE001 - intentional broad catch by design
                last_exception = exc
                logger.warning("Attempt %s/%s failed: %s", attempt, attempts, exc)
                if attempt < attempts:
                    time.sleep(current_delay)
                    current_delay *= backoff_factor

        raise RetryExhaustedError(f"Action failed after {attempts} attempts") from last_exception

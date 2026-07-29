"""
exceptions.py

Custom exception hierarchy for the framework. Using dedicated exception
types (rather than bare ``AssertionError`` or ``Exception``) makes test
failures self-documenting in reports/logs and lets calling code catch
specific failure categories when needed.
"""


class FrameworkError(Exception):
    """Base class for every exception raised by this framework."""


class ConfigurationError(FrameworkError):
    """Raised when required configuration is missing or invalid."""


class ElementNotFoundError(FrameworkError):
    """Raised when a required UI element cannot be located within timeout."""


class ElementNotInteractableError(FrameworkError):
    """Raised when an element is found but cannot be clicked/filled/etc."""


class PageLoadError(FrameworkError):
    """Raised when a page fails to reach the expected ready state."""


class DataLoadError(FrameworkError):
    """Raised when test data (JSON/YAML/CSV) cannot be loaded or parsed."""


class RetryExhaustedError(FrameworkError):
    """Raised when a retried operation fails after all attempts are used."""


class AssertionHelperError(FrameworkError):
    """Raised by AssertionHelper when a soft/hard assertion fails."""

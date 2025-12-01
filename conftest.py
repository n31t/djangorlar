# Python modules
import pytest
from typing import Any


@pytest.fixture(scope='session')
def django_db_setup() -> None:
    """Configure database for testing."""
    pass


@pytest.fixture
def Settings() -> dict[str, Any]:
    """Provide test settings."""
    return {
        'DEBUG': True,
    }

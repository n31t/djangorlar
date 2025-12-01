import pytest
from typing import Any

@pytest.fixture(scope='session')
def django_db_setup() -> None:
    """Set up the django database for the tests"""
    pass

@pytest.fixture
def Settings() -> dict[str, Any]:
    """Return the django settings for the tests"""
    return {
        'DEBUG': True,
    }
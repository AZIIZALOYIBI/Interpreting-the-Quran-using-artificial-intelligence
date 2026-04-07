"""
Shared pytest fixtures for the Quran AI backend tests.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture(scope="module")
def client():
    """FastAPI test client shared across all tests in a module."""
    with TestClient(app) as c:
        yield c

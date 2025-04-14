import pytest


@pytest.fixture
def demo_api():
    url = 'http://10.86.97.157:8000/api'
    return url
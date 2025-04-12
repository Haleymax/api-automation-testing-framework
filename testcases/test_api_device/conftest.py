import pytest

from config import setting
from data.generate_case import generate_case


@pytest.fixture(scope="session")
def url():
    url = f'testscripts/audio/test.js'
    return url

@pytest.fixture(scope="session")
def add_device_url(url):
    host = setting.HSOT
    port = setting.PORT
    url = f'http://{host}:{port}/device/add_device'
    return url

@pytest.fixture(scope="session")
def del_device_url(url):
    host = setting.HSOT
    port = setting.PORT
    url = f'http://{host}:{port}/device/del_device'
    return url

api_case = generate_case(setting.YAML_FILE_PATH)
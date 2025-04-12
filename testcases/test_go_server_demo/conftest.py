import pytest

from config import setting
from data.generate_case import generate_case


@pytest.fixture(scope='session')
def add_api():
    server = setting.GO_SERVER
    url = server + "/api/v1/device/add"
    return url

@pytest.fixture(scope='session')
def del_api():
    server = setting.GO_SERVER
    url = server + "/api/v1/device/delete"
    return url


api_case = generate_case(setting.YAML_FILE_PATH)
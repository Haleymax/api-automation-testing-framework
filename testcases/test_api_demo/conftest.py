import pytest
import urllib3

from config import setting
from data.generate_case import generate_case



@pytest.fixture(scope='module')
def demo_api():
    url = 'http://10.86.97.157:8000/demo'
    yield url
    print("测试完成")




api_case = generate_case(setting.YAML_FILE_PATH)
import json

import pytest

from core.sender import Sender
from testcases.test_go_server_demo.conftest import api_case


class TestDELAPI:

    @pytest.mark.name('test add api')
    @pytest.mark.api
    @pytest.mark.parametrize("host, name, user, password", api_case['add_device'])
    def test_add_api(self, host, name, user, password, rp_logger, del_api):
        rp_logger.info("run delete api")
        rp_logger.info(f"host: {host}")
        sender = Sender()
        sender.delete(url=del_api, params={"host": host})
        rp_logger.info(f"quest time {sender.request_time}")
        rp_logger.info(sender.result)
        rp_logger.info(f"response : {sender.response}")
        rp_logger.info(f"response time {sender.request_time}")
        assert sender.response.status_code == 200
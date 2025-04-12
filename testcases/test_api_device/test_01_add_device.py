import pytest

from core.sender import Sender
from testcases.test_api_device.conftest import api_case


class TestRunApiTC:
    @pytest.mark.name("test add device api")
    @pytest.mark.api
    @pytest.mark.parametrize("host, name, user, password",api_case["add_device"])
    def test_01_run_tc(self, host, name, user, password, add_device_url, rp_logger):
        rp_logger.debug(f"Running test add device {host} with API {add_device_url}")
        rp_logger.info("run add device api")
        rp_logger.info(f"host: {host} , name: {name} , user: {user} , password: {password}")
        post_data = {
            "host": host,
            "name": name,
            "user": user,
            "password": password
        }
        sender = Sender()
        sender.post(add_device_url, json=post_data)
        rp_logger.info(f"quest time {sender.request_time}")
        rp_logger.info(sender.result)
        assert sender.check_status(), sender.result["message"]

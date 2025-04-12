import pytest

from core.sender import Sender
from testcases.test_api_device.conftest import api_case


class TestRunApiTC:
    @pytest.mark.name("test delete device api")
    @pytest.mark.api
    @pytest.mark.parametrize("host",api_case["del_device"])
    def test_01_run_tc(self, host, del_device_url, rp_logger):
        host = host[0]
        rp_logger.debug(f"Running test add device {host} with API {del_device_url}")
        rp_logger.info("run add delete api")
        rp_logger.info(f"host: {host}")
        sender = Sender()
        sender.delete(del_device_url, params=f"host={host}")
        rp_logger.info(f"quest time {sender.request_time}")
        rp_logger.info(sender.result)
        assert sender.check_status(), sender.result["message"]

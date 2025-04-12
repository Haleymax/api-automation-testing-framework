import re
import time

import requests

from core.logger import logger


def extract_ip_address(input_string):
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    result = re.search(pattern, input_string)
    if result:
        return result.group(0)
    return None


class Sender:
    def __init__(self):
        self.session = requests.Session()
        self.response = None
        self.result = None
        self.request_time = None

    def get(self, url, params=None, headers=None):
        try:
            start_time = time.time()
            self.response = self.session.get(url, params=params, headers=headers)
            end_time = time.time()
            self.request_time = end_time - start_time
            logger.info(f"successful send get request to : {url}")
        except Exception as e:
            logger.info(f"request failed : {e}")

    def post(self, url, params=None, data=None, json=None, headers=None):
        try:
            start_time = time.time()
            self.response = self.session.post(
                url,
                params=params,
                data=data,
                json=json,
                headers=headers
            )
            end_time = time.time()
            logger.info(f"successful send post request to : {url}")
            self.result = self.response.json()
            self.request_time = end_time - start_time
            return True  # 或者返回 self.response
        except Exception as e:
            logger.error(f"request failed : {e}")  # 错误级别建议用 error
            return False  # 或者 raise 重新抛出异常

    def delete(self, url, params=None, headers=None):
        try:
            start_time = time.time()
            self.response = self.session.delete(url, params=params, headers=headers)
            end_time = time.time()
            logger.info(f"successful send delete request to : {url}")
            self.request_time = end_time - start_time
            self.result = self.response.json()
            return True
        except Exception as e:
            logger.error(f"request failed : {e}")
            return False

    def check_status(self):
        """
        检查修改是否成功
        :return: HTTP 状态码
        """
        return self.result["status"]

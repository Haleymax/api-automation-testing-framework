from config import setting

import requests


class ReportPanel:
    def __init__(self):

        self.base_url = f"http://10.86.97.157:8080/api/v1/{setting.REPORT_PROJECT}"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {setting.REPORTPORTAL_TOKEN}",
            "Content-Type": "application/json"
        }
        self.widget_id = 61
        self.filter_id = 60

    def create_filter(self, launch_number, case_name):
        """
        创建ReportPortal过滤器来筛选特定编号的测试用例

        参数:
            launch_number (int): 要筛选的测试用例编号
            project_name (str): ReportPortal项目名称，默认为"default"
            token (str): ReportPortal API访问令牌

        返回:
            dict: API响应结果
        """
        api = self.base_url+"/filter"
        data = {
            "description": f"Filter for launch number {launch_number}",
            "name": f"launch_{launch_number}_filter",
            "type": "launch",  # 筛选测试执行(launch)
            "conditions": [
                {
                    "filteringField": "number",  # 筛选编号字段
                    "condition": "eq",  # 等于条件
                    "value": str(launch_number)  # 转换为字符串
                },
                {
                    "filteringField": "name",  # 筛选编号字段
                    "condition": "eq",  # 等于条件
                    "value": case_name  # 转换为字符串
                }
            ],
            "orders": [
                {
                    "sortingColumn": "startTime",  # 按开始时间排序
                    "isAsc": True  # 降序排列(最新的在前)
                }
            ]
        }

        try:
            response = requests.post(api, headers=self.headers, json=data)
            if response.status_code in [200,201]:
                self.filter_id = response.json()["id"]
            else:
                raise ValueError(response.text)
        except Exception as e:
            print(f"创建过滤器失败: {e}")

    def create_widget(self):
        if self.filter_id == 0:
            raise ValueError("the filter does not exist, please create a new filter")

        api = self.base_url+"/widget"
        widget_data = {
            "description": "test_widget",
            "name": "test2",
            "widgetType": "launchesTable",
            "contentParameters": {
                "contentFields": [
                    "name", "date", "status"
                ],
                "columnWidths": {
                    "name": 200,
                    "data": 150,
                    "statis" : 100
                },
                "itemsCount": 50,  # 修改为1-600之间的值
                "widgetOptions": {
                    "timeline": "1_week",
                    "chartType": "line"
                }
            },
            "filterIds": [
                self.filter_id
            ]
        }
        response = requests.post(api, headers=self.headers, json=widget_data)
        if response.status_code in [200,201]:
            self.widget_id = response.json()["id"]
        else:
            raise ValueError(response.text)

    def create_dashboard(self, name, description):
        dashboard_data = {

        }

if __name__ == '__main__':
    re = ReportPanel()
    re.create_widget()
    print(re.widget_id)
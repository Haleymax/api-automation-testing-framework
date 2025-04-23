from typing import Optional, Dict, Any
import requests
from config import setting
from core.logger import logger


class ReportPortalError(Exception):
    """ReportPortal操作异常基类"""
    pass


class ReportPanel:
    def __init__(self, base_url: Optional[str] = None, project: Optional[str] = None, token: Optional[str] = None):
        """
        初始化ReportPortal操作类

        Args:
            base_url: ReportPortal基础URL"
            project: 项目名称
            token: API访问令牌
        """
        self.base_url = base_url or f"http://10.86.97.157:8080/api/v1/{setting.REPORT_PROJECT}"
        self.token = token or setting.REPORTPORTAL_TOKEN

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.widget_id: Optional[str] = None
        self.filter_id: Optional[str] = None
        self.dashboard_id: Optional[str] = None

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        统一的请求方法

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE)
            endpoint: API端点路径
            **kwargs: 其他requests参数

        Returns:
            dict: 解析后的JSON响应

        Raises:
            ReportPortalError: 当请求失败时抛出
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # 自动处理4xx/5xx错误
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"API请求失败: {method} {url} - {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f", 响应: {e.response.text}"
            raise ReportPortalError(error_msg)

    def create_filter(self, launch_number: int, case_name: str, filter_name: Optional[str] = None,
                      description: Optional[str] = None) -> str:
        """
        创建用于筛选特定测试用例的过滤器

        Args:
            launch_number: 要筛选的测试编号
            case_name: 要筛选的用例名称
            filter_name: 过滤器名称(可选)
            description: 过滤器描述(可选)

        Returns:
            str: 创建的过滤器ID

        Raises:
            ReportPortalError: 当创建失败时抛出
        """
        if not filter_name:
            filter_name = f"launch_{launch_number}_{case_name}_filter"
        if not description:
            description = f"筛选测试编号 {launch_number} 和用例 {case_name}"

        data = {
            "description": description,
            "name": filter_name,
            "type": "launch",
            "conditions": [
                {"filteringField": "number", "condition": "eq", "value": str(launch_number)},
                {"filteringField": "name", "condition": "eq", "value": case_name}
            ],
            "orders": [{"sortingColumn": "startTime", "isAsc": True}]
        }

        try:
            result = self._make_request("POST", "filter", json=data)
            self.filter_id = result["id"]
            logger.info(f"成功创建过滤器: {self.filter_id}")
            return self.filter_id
        except Exception as e:
            raise ReportPortalError(f"创建过滤器失败: {str(e)}")

    def create_widget(self, name: str, widget_type: str = "launchesTable",
                      description: Optional[str] = None) -> str:
        """
        创建仪表板组件

        Args:
            name: 组件名称
            widget_type: 组件类型，默认为"launchesTable"
            description: 组件描述(可选)

        Returns:
            str: 创建的组件ID

        Raises:
            ReportPortalError: 当创建失败或缺少过滤器时抛出
        """
        if not self.filter_id:
            raise ReportPortalError("需要先创建过滤器")

        if not description:
            description = f"{name} 组件"

        widget_data = {
            "description": description,
            "name": name,
            "widgetType": widget_type,
            "contentParameters": {
                "contentFields": [
                    "name",
                    "startTime",
                    "endTime",
                    "status",
                    "statistics$executions$total",
                    "statistics$executions$passed",
                    "statistics$executions$failed"
                ],
                "columnWidths": {"name": 200, "data": 150, "statis": 100},
                "itemsCount": 50,
                "widgetOptions": {
                    "viewModel": "bar",
                    "launchNameFilter": "",
                    "sortBy": "startTime",
                    "sortOrder": "DESC",
                }
            },
            "filterIds": [self.filter_id]
        }

        try:
            result = self._make_request("POST", "widget", json=widget_data)
            self.widget_id = result["id"]
            logger.info(f"成功创建组件: {self.widget_id}")
            return self.widget_id
        except Exception as e:
            raise ReportPortalError(f"创建组件失败: {str(e)}")

    def create_dashboard(self, name: str, description: Optional[str] = None) -> str:
        """
        创建仪表板

        Args:
            name: 仪表板名称
            description: 仪表板描述(可选)

        Returns:
            str: 创建的仪表板ID

        Raises:
            ReportPortalError: 当创建失败时抛出
        """
        if not description:
            description = f"{name} 仪表板"

        dashboard_data = {
            "name": name,
            "description": description
        }

        try:
            result = self._make_request("POST", "dashboard", json=dashboard_data)
            self.dashboard_id = result["id"]
            logger.info(f"成功创建仪表板: {self.dashboard_id}")
            return self.dashboard_id
        except Exception as e:
            raise ReportPortalError(f"创建仪表板失败: {str(e)}")

    def generate_dashboard(self, widget_name: Optional[str] = None) -> bool:
        """
        向仪表板添加组件

        Args:
            widget_name: 组件名称(可选)，默认为"Widget_{widget_id}"

        Returns:
            bool: 是否成功添加

        Raises:
            ReportPortalError: 当操作失败或缺少必要资源时抛出
        """
        if not all([self.dashboard_id, self.widget_id, self.filter_id]):
            raise ReportPortalError("需要先创建仪表板、组件和过滤器")

        if not widget_name:
            widget_name = f"Widget_{self.widget_id}"

        endpoint = f"dashboard/{self.dashboard_id}/add"
        add_widget_data = {
            "addWidget": {
                "widgetId": int(self.widget_id),  # 转换为整数
                "widgetName": widget_name,
                "widgetType": "launches_table",
                "widgetSize": {
                    "width": 12,  # 默认宽度
                    "height": 6  # 默认高度
                },
                "widgetPosition": {
                    "positionX": 0,  # 默认X位置
                    "positionY": 0  # 默认Y位置
                },

                "filters": [int(self.filter_id)]
            }
        }

        try:
            # 根据文档使用PUT方法
            self._make_request("PUT", endpoint, json=add_widget_data)
            logger.info(f"成功将组件 {widget_name}(ID:{self.widget_id}) 添加到仪表板 {self.dashboard_id}")
            return True
        except Exception as e:
            raise ReportPortalError(f"添加组件到仪表板失败: {str(e)}")

    def cleanup(self):
        """清理创建的所有资源"""
        resources = []
        if self.dashboard_id:
            resources.append(("dashboard", self.dashboard_id))
        if self.widget_id:
            resources.append(("widget", self.widget_id))
        if self.filter_id:
            resources.append(("filter", self.filter_id))

        for resource_type, resource_id in resources:
            try:
                self._make_request("DELETE", f"{resource_type}/{resource_id}")
                logger.info(f"成功删除{resource_type}: {resource_id}")
            except ReportPortalError as e:
                logger.warning(f"删除{resource_type} {resource_id} 失败: {str(e)}")

        # 重置所有ID
        self.dashboard_id = None
        self.widget_id = None
        self.filter_id = None


if __name__ == '__main__':
    try:
        # 示例用法
        report = ReportPanel()

        # 1. 创建过滤器
        filter_id = report.create_filter(
            launch_number=10,
            case_name="demo_test",
            filter_name="演示过滤器"
        )

        # 2. 创建组件
        widget_id = report.create_widget(
            name="演示组件",
            widget_type="launchesTable",
            description="用于展示测试结果的组件"
        )

        # 3. 创建仪表板
        dashboard_id = report.create_dashboard(
            name="演示仪表板",
            description="测试报告展示"
        )

        # 4. 向仪表板添加组件
        report.generate_dashboard(widget_name="测试结果展示")
    except ReportPortalError as e:
        logger.error(f"操作失败: {e}")
        report.cleanup()
    except Exception as e:
        logger.error(f"发生未预期错误: {e}")
        report.cleanup()
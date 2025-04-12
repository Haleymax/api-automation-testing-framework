# API 自动化框架

## 1. 安装依赖
### 1.1 reportportal
需要使用的报告工具 `reportportal`
```shell
cd docker
# 直接docker拉取
docker compose -p reportportal up -d
```

添加配置文件`pytest.ini`
```ini
[pytest]
rp_api_key = xxxxxxxxxxx #reportportal生成的api
rp_endpoint = http://127.0.0.1:8080   #自动部署的服务地址
rp_project = xxxx  # 项目名称
rp_launch = xxxxxx # 启动名称
```

### 1.2 安装Python依赖
```shell
pip install -r requirements.txt
```


## 2. 运行项目
```shell
# 指定到具体需要运行的case
pytest xxxxx.py --reportportal
```
# 阿里云动态域名解析

- 帮助文档
  - 阿里云解析`API`文档: https://next.api.aliyun.com/api-tools/sdk/Alidns?version=2015-01-09&language=python-tea&tab=primer-doc

  - 阿里云密钥管理文档: https://help.aliyun.com/document_detail/116401.htm

  - 阿里云解析请求接口服务地址: https://next.api.aliyun.com/product/Alidns
- 环境要求: `python >= 3.9`

- 克隆源文件

  ```sh
  git clone https://github.com/L00N9CHEN/Aliddns.git
  ```

- 第三方库: `PyYAML`, `alibabacloud_alidns20150109`, `requests`

  ```sh
  # 进入Aliddns目录,创建虚拟隔离环境
  python3 -m venv env
  # 激活虚拟隔离环境
  source env/bin/activate
  # 在虚拟隔离环境下安装第三方库
  pip install -r requirements.txt
  ```

- 配置文件路径: `Aliddns/config/config.yaml`, 首次运行会通过示例模板创建,修改相应参数后再运行.

  ```yaml
  RegionEndpoint: "alidns.cn-shenzhen.aliyuncs.com"
  AccessKeyID: "Your Access Key ID"
  AccessSecret: "Your Access Key Secret"
  DomainName: "example.com"
  RecordKeyword: "test"
  RecordType: "A"
  ```

- 日志记录按天轮转日志文件并保留最近90天的日志, 文件路径: `Aliddns/logs/`

- 运行

  ```python
  python main.py
  ```

- 创建任务计划

  - Linux

    > 假定已经源文件克隆到用户家目录,使用 `crontab -e` 编辑任务调度,每**2**小时运行一次

    ```ini
    0 */2 * * * $HOME/Aliddns/env/bin/python $HOME/Aliddns/main.py
    ```

  - Windows

    > 参考官方文档: https://learn.microsoft.com/zh-cn/windows/win32/taskschd/task-scheduler-start-page


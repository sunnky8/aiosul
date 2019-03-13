import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = {
    # 部署机器的IP
    "HOST": '0.0.0.0',
    # 端口
    "PORT": 9000,
    "PROJECTNAME": "consul-demo",
    "CONSUL_TAG": ['aiohttp-mico-service'],
    "CONSUL_HOST": '127.0.0.1',
    "CONSUL_PORT": 8500,
}

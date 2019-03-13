import logging
import socket

from config import config
from utils.consul_client import ConsulClient

logger = logging.getLogger(__file__)


def register_consul():
    try:
        httpcheck = 'http://' + get_ip() + ':' + str(config['PORT']) + '/check'
        service_id = config['PROJECTNAME'] + get_ip() + ':' + str(config['PORT'])
        # 注册服务到consul,不需要则注释
        ConsulClient(host=config['CONSUL_HOST'], port=config['CONSUL_PORT']).register(
            name=config['PROJECTNAME'], service_id=service_id,
            address=config['HOST'],
            port=config['PORT'], tags=config['CONSUL_TAG'],
            interval='30s',
            httpcheck=httpcheck)
    except Exception as e:
        logger.error(e)


def deregister_consul():
    try:
        service_id = config['PROJECTNAME'] + config['HOST'] + ':' + str(config['PORT'])
        ConsulClient(host=config['CONSUL_HOST'], port=config['CONSUL_PORT']).deregister(service_id)
    except Exception as e:
        logger.error(e)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]

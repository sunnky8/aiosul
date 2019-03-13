import datetime
import decimal
import json

from aiohttp import web

from config import config
from utils.consul_client import ConsulClient


class RewriteJsonEncoder(json.JSONEncoder):
    """重写json类，为了解决datetime类型的数据无法被json格式化"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif hasattr(obj, 'isoformat'):
            # 处理日期类型
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


def json_dumps(obj):
    return json.dumps(obj, cls=RewriteJsonEncoder)


class ServiceView(web.View):

    async def get(self):
        """列出所有服务"""
        client = ConsulClient(config['CONSUL_HOST'], config['CONSUL_PORT'])
        name = self.request.rel_url.query.get('name')
        if not name:
            services = client.get_services()
            return web.json_response(data=services, dumps=json_dumps)
        service = await client.get_service_by_name(name)
        return web.json_response(data=service, dumps=json_dumps)


async def check(request):
    return web.Response(text='success')

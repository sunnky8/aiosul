from random import randint

import aiohttp
from consulate import Consul


class ConsulClient():
    def __init__(self, host=None, port=None, token=None):
        self.host = host
        self.port = port
        self.token = token
        self.consul = Consul(host=host, port=port)

    def register(self, name, service_id, address, port, tags, interval, httpcheck):
        self.consul.agent.service.register(name, service_id=service_id, address=address, port=port, tags=tags,
                                           interval=interval, httpcheck=httpcheck)

    def deregister(self, service_id):
        self.consul.agent.service.deregister(service_id)
        self.consul.agent.check.deregister(service_id)

    async def get_service_by_name(self, name):
        available_services = []
        async with aiohttp.ClientSession() as session:
            url = 'http://{}:{}/v1/health/service/{}'.format(self.host, self.port, name)
            async with session.get(url) as resp:
                services = await resp.json()
                for s_data in services:
                    print(s_data)
                    status = s_data.get('Checks')[0].get('Status')
                    if status == 'passing':
                        address = s_data.get('Service').get('Address')
                        port = s_data.get('Service').get('Port')
                        available_services.append({'port': port, 'address': address})

            if not available_services:
                raise Exception('no service can be used')
            else:
                service = available_services[randint(0, len(available_services) - 1)]
                return {"host": service['address'], "port": int(service['port'])}

    def get_services(self):
        return self.consul.agent.services()

from aiohttp import web

from app.routers import setup_routes
from config import config
from utils.consul import register_consul


app = web.Application()
setup_routes(app)
register_consul()
web.run_app(app, host=config['HOST'], port=config['PORT'])

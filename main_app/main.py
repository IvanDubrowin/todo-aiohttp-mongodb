import hashlib
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from motor import motor_asyncio as ma
from routes import setup_routes
from middlewares import authorize
from settings import *


middle = [
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest())),
    authorize,
]

app = web.Application(middlewares=middle)
setup_routes(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_ROOT))

app['static_root_url'] = STATIC_ROOT

app.client = ma.AsyncIOMotorClient(MONGO_HOST)
app.db = app.client[MONGO_DB_NAME]

if __name__ == '__main__':
    web.run_app(app, host=SITE_HOST, port=SITE_PORT)

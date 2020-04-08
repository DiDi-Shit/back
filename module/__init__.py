import asyncpg
import base64
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from utils import *
import os.path as path
from .login import signup, signin
from .getToilet import getToilet
from .sample import *

async def initapp(config):
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    app['config'] = load_config(config)
    dbconfig = app['config']['db']
    
    app['pool'] = await asyncpg.create_pool(user=app['config']['db']['user'], database=app['config']['db']['database'], password=dbconfig['password'])
    app.router.add_get('/', hello)
    app.router.add_post('/login', signin)
    app.router.add_post('/signup', signup)
    app.router.add_post('/getToilet', getToilet)
    return app
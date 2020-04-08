import aiohttp
import asyncpg
import asyncio
import base64
import aiohttp_session
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from utils import *
import os.path as path
import time
import geohash
from math import radians, cos, sin, asin, sqrt
import module

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(module.initapp(
        path.join(path.dirname(__file__), 'config.yml')))
    web.run_app(app, port=6800)

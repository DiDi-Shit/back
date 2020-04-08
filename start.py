import asyncio
from aiohttp import web
import os.path as path
import module

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(module.initapp(
        path.join(path.dirname(__file__), 'config.yml')))
    web.run_app(app, port=6800)

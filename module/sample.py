import aiohttp
import asyncpg
import asyncio
import base64
import aiohttp_session
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import time


async def lastVisit(request):
    session = await get_session(request)
    if "las" in session:
        last = session["las"]
    else:
        last = "none"
    session["las"] = time.time()
    return web.Response(text=f"last visit at {last}")


async def hello(request):
    pool = request.app["pool"]
    try:
        async with pool.acquire() as conn:
            await conn.execute("insert into test values (12)")
    except:
        return web.Response(text="insert failed")
    return web.Response(text="insert successful!")


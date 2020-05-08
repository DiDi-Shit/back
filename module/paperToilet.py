pip install aiohttp
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
import requests

async def Create_Order(request):
    pool = request.app["pool"]
    data = await request.post()
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                 "insert into deliverrecord values ({},{},'{}');".format(data["id"], data["tid"],data["statement"])
            )
    except asyncpg.exceptions.UniqueViolationError:
        return web.Response(text="Already exist")
    return web.Response(text="create order.")

async def Query_Order(request):
    pool = request.app["pool"]
    data = await request.post()
    try:
        async with pool.acquire() as conn:
            values = await conn.fetch(
                "select * from deliverrecord where app = ({},{});".format(data["id"],data["tid"])
            )
    except:
        return web.Response(text="no.") 
    return web.Response(text="yes.") 
 
 async def Delete_Order(request):
    pool = request.app["pool"]
    data = await request.post()
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                 "delete from deliverrecord where app=({},{});".format(data["id"],data["tid"])
            )
    except:
        return web.Response(text="delete failed")
    return web.Response(text="delete order.")  
   
 async def Update_Order(request):
    pool = request.app["pool"]
    data = await request.post()
     try:
        async with pool.acquire() as conn:
            await conn.execute(
                "update deliverrecord set values ('{}')where app=({},{});".format(data["statement"],data["id"],data["tid"])
            )
    except:
       return web.Response(text="update failed.") 
    return web.Response(text="update order.")





  
 


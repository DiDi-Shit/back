from aiohttp import web
import geohash
from random import randint
import asyncpg


async def addToilet(request):
    pool = request.app["pool"]
    data = await request.post()
    try:
        w = float(data["w"])
        j = float(data["j"])
    except:
        data = request.query
        w = float(data["w"])
        j = float(data["j"])
    geo = geohash.encode(w, j)
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                """insert into geo values ({},{},{},'{}')""".format(
                    "DEFAULT", w, j, geo
                )
            )
    except asyncpg.exceptions.UniqueViolationError:
        return web.Response(text="Already exist")
    return web.Response(text="ok")

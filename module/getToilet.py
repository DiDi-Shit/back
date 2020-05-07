from aiohttp import web
import geohash
import asyncpg
from utils import haversine


def getN(geo) -> list:
    w, j = geohash.decode(geo)
    wdelta = [0.0027, -0.0027, 0]
    jdelta = [0.0055, -0.0055, 0]
    return [
        geohash.encode(x * 2 + w, y * 2 + j) for x in wdelta for y in jdelta if x != y
    ]


async def getToilet(request):
    pool = request.app["pool"]
    data = await request.post()
    try:
        maxSize = int(data["mx"])
        w = float(data["w"])
        j = float(data["j"])
    except:
        data = request.query
        maxSize = int(data["mx"])
        w = float(data["w"])
        j = float(data["j"])
    geo = geohash.encode(w, j)
    neib = getN(geo)
    neib.append(geo)
    sql = ""
    for item in neib:
        sql += f"or geo like '{item[:6]}%' "
    sql = sql[3:]
    try:
        async with pool.acquire() as conn:
            values = await conn.fetch("select * from geo where " + sql)
            to = [[x["tid"], x["w"], x["j"]] for x in values]
            to.sort(
                key=lambda x: haversine(float(j), float(w), float(x[1]), float(x[2]))
            )
            res = {"mx": min(maxSize, len(to)), "ans": to[:maxSize]}
    except asyncpg.exceptions.UniqueViolationError:
        return web.Response(text="Already exist")
    return web.json_response(data=res)


async def acquireToilet(app, sql, args):
    pool = app["pool"]
    try:
        async with pool.acquire() as conn:
            values = await conn.fetch(sql, args)
            return values
    except asyncpg.exceptions.UniqueViolationError:
        return web.Response(text="Some Bug here")

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


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def getN(geo) -> list:
    w, j = geohash.decode(geo)
    wdelta = [0.0027, -0.0027, 0]
    jdelta = [0.0055, -0.0055, 0]
    return [geohash.encode(x*2+w, y*2+j)for x in wdelta for y in jdelta if x != y]


async def lastVisit(request):
    session = await get_session(request)
    if 'las' in session:
        last = session['las']
    else:
        last = "none"
    session['las'] = time.time()
    return web.Response(text=f"last visit at {last}")


async def login(request):
    data = await request.post()
    pool = request.app['pool']
    try:
        async with pool.acquire() as conn:
            values = await conn.fetch('select * from test where app = {};'.format(data['usr']))
            if len(values) == 0 or values[0]['pass'] != data['pass']:
                raise Exception
    except:
        return web.Response(text='login failed')
    return web.Response(text="ok")


async def signup(request):
    pool = request.app['pool']
    data = await request.post()
    try:
        async with pool.acquire() as conn:
            await conn.execute('insert into test values ({},\'{}\');'.format(data['usr'], data['pass']))
    except asyncpg.exceptions.UniqueViolationError:
        return web.Response(text='Already exist')
    return web.Response(text='Insert Ok. User Created.')


async def getToilet(request):
    pool = request.app['pool']
    data = await request.post()
    maxSize = int(data['mx'])
    w = float(data['w'])
    j = float(data['j'])
    geo = geohash.encode(w, j)
    neib = getN(geo)
    sql = ""
    for item in neib:
        sql += f"or geo like '{item[:6]}%' "
    sql = sql[3:]
    try:
        async with pool.acquire() as conn:
            values = await conn.fetch("select * from geo where "+sql)
            to = [[x['tid'], x['w'], x['j']] for x in values]
            to.sort(key=lambda x: haversine(j, w, x[1], x[2]))
            res={"mx":min(maxSize,len(to)),"ans":to[:maxSize]}
    except asyncpg.exceptions.UniqueViolationError:
        return web.Response(text='Already exist')
    return web.json_response(data=res)


async def hello(request):
    pool = request.app['pool']
    try:
        async with pool.acquire() as conn:
            await conn.execute('insert into test values (12)')
    except:
        return web.Response(text='insert failed')
    return web.Response(text='insert successful!')


async def initapp():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    app['config'] = load_config(
        path.join(path.dirname(__file__), 'config.yml'))
    dbconfig = app['config']['db']
    app['pool'] = await asyncpg.create_pool(user=app['config']['db']['user'], database=app['config']['db']['database'], password=dbconfig['password'])
    app.router.add_get('/', hello)
    app.router.add_post('/login', login)
    app.router.add_post('/signup', signup)
    app.router.add_post('/getToilet', getToilet)
    return app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(initapp())
web.run_app(app, port=6800)

import copy
import asyncio
import asyncpg
import json
from aiohttp import web
class Operate:
    def __init__(self):
        self.res=''
        
        
        
        
 
    
    async def get_deliver_record(self,id,tid):#查询送纸记录(id,tid)
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        self.res = await conn.fetch(
            'SELECT distinct * FROM deliverrecord where deliverrecord.id = $1 and deliverrecord.tid = $2', id, tid)
        await conn.close()

    async def get_shit_record(self,id,tid):#查询拉屎记录(id,tid)
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        self.res = await conn.fetch(
            'SELECT distinct * FROM shitrecord where shitrecord.id=&1 and shitrecord.tid=&2',id,tid)
        await conn.close()
    
    async def get_Toliet_all(self):#所有厕所信息
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        self.res = await conn.fetch(
            'SELECT distinct * FROM toliet')
        await conn.close()
        
    
    async def get_Users_personal(self,id):#个人信息根据id
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        self.res = await conn.fetchrow(
            'SELECT distinct * FROM uesrs where id=&1',id)
        await conn.close()
        
        
    async def add_Users(self,id,name,sex):#增加用户（注册）
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        await conn.execute('''
                INSERT INTO users(id, name,sex) VALUES($1, $2,$3)
            ''', id,name,sex)
        await conn.close()

    async def add_Toliet(self,w,j,geo):#增加厕所（注册）
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        await conn.execute("""insert into toliet values (DEFAULT,$1,$2,$3)"""
                    , w, j, geo)
        await conn.close()
    async def add_Deliverrecord(self,id,tid,statement):#增加送纸记录
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        await conn.execute('''
                INSERT INTO deliverrecord(id,tid,statement) VALUES($1, $2, $3)
            ''', id,tid,statement)
        await conn.close()
    async def add_shitrecord(self,id,tid,comment=''):#增加拉屎记录
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        await conn.execute('''
                INSERT INTO shitrecord(id, tid, comment) VALUES($1, $2,$3)
            ''', id,tid,comment)
        await conn.close()
   
    async def get_Toliet_Comment(self,tid):#查询厕所评价
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        self.res = await conn.fetchrow(
            'SELECT distinct shitrecord.comment FROM shitrecord where tid=$1',tid)
        await conn.close()

        
    async def get_Toliet_Location(self,tid):#查询厕所位置
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        self.res = await conn.fetchrow(
            'SELECT distinct toliet.geo FROM toliet where tid=$1',tid)
        await conn.close()

    async def delete_Deliverrecord(self,id,tid):#删除送纸记录
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        await conn.execute('''delete from  deliverrecord where id=$1 and tid=$2''',id,tid)
        await conn.close()
        
    async def update_Deliverrecord(self,id,tid,statement):#更新备注
        conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
                                     database='Didishit')
        await conn.execute('''update deliverrecord set statement=$1 where id=$2 and tid=$3''',statement,id,tid)
        await conn.close()

id=1
tid=3
sex="nan"
w={''}
j={''}
geo={" "}
statement='www'
name="jjj"

# loop = asyncio.get_event_loop()
# loop.run_until_complete(t.add_Users(id,name,sex))
# loop = asyncio.get_event_loop()
# loop.run_until_complete(t.add_Toliet(w,j,geo))
t=Operate() #类的建立
loop = asyncio.get_event_loop()
#***函数的调用如：
loop.run_until_complete(t.get_Toliet_Comment(tid))
print(t.res)#查询结果存在t.res中



   
    # async def run(self):#自我测试函数
    #     conn = await asyncpg.connect(user='hxx', password='zxcZXC123',
    #                                 database='Didishit')
    # # values = await conn.fetch('''SELECT * FROM test''')
    # #     await conn.execute('''CREATE TABLE users(id serial PRIMARY KEY, name text, dob date)''')

    #     #Insert a record into the created table.
    #     #await self.connectpool()
    #     await self.pool.execute('''
    #             INSERT INTO test(id, num,data) VALUES($1, $2,$3)
    #         ''', 2,123456,"jjjj")

    #     #Select row from the table.
    #     #fetchrow,fetch
        
    #     self.res = await self.pool.fetch(
    #         'SELECT * FROM test ')
        
        #await pool['pool'].close()


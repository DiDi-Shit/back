import asyncio
import asyncpg
import json 
from aiohttp import web

async def Create_Order(user,wcid,remark):#创建订单时还未付款
     conn = await asyncpg.connect(user='hxx', password='zxcZXC123', database='Didishit')
     await pool.execute('''insert into deliverrecord (id,tid,statement) VALUES ($1,$2,$3,$4)''',user,wcid,remark)
     await conn.close()
async def Delete_Order(user,wcid):#删除相关订单
     conn = await asyncpg.connect(user='hxx', password='zxcZXC123', database='Didishit')
       await pool.execute('''delete from  deliverrecord where user=id and wcid=tid''')
     await conn.close()
async def Update_Order(user,wcid,remark):#修改订单的备注信息
     conn = await asyncpg.connect(user='hxx', password='zxcZXC123', database='Didishit')
     await pool.execute("update deliverrecord set statement=remark where user=id and wcid=tid'",remark)
     await conn.close()
async def Query_Order(user,wcid):#查询相关订单
     conn = await asyncpg.connect(user='hxx', password='zxcZXC123', database='Didishit')
     res=await conn.fetch('select * from deliverrecord where user=id and wcid=tid',id,tid)
     await conn.close()

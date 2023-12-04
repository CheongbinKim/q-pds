from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from autocall.singleCall import SingleCall
from autocall.multiCall import MultiCall
import transaction

import asyncio

sgCall = SingleCall()
mtCall = MultiCall()

serverRouter = APIRouter(prefix='/server', tags=['/server'])

@serverRouter.on_event("startup")
async def on_startup():
    asyncio.create_task(sgCall.run())
    #asyncio.create_task(mtCall.run())

@serverRouter.get("/status")
async def serverStatus():
    rtnParam = transaction.recentScheStat()
    return JSONResponse(content=rtnParam[0])

@serverRouter.get("/start",status_code=200)
async def start():
    param = {"stat":"1"}
    rtnParam = transaction.regScheStat(param)
    #sgCall.start()
    return JSONResponse(content={})

@serverRouter.get("/stop",status_code=200)
async def stop():
    param = {"stat":"0"}
    rtnParam = transaction.regScheStat(param)
    #sgCall.stop()
    return JSONResponse(content={})
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import transaction
from pydantic import BaseModel
from datetime import datetime

class ScheduleManager(BaseModel):
    seq: int
    sid: str = None
    scheDt: str = None
    phnNum:str = None


callRouter = APIRouter(prefix='/call')
 
@callRouter.get("/list",tags=["/call"])
async def callList():
    # 1. get call List form api Server
    # 2. reg call List in db
    # 3. get call List from db
    c1 = transaction.readWaitingSchedule()
    # lists = []
    # json_compatible_item_data = jsonable_encoder(c1)
    # lists.append(json_compatible_item_data)
    return JSONResponse(content=c1)

    #lists = [{'sid':'sid123','number':'01064498979','state':'0','stateName':'대기중'}]
    #return JSONResponse(content=lists)

@callRouter.post("/addNumber",tags=["/call"])
async def addNumber(request: Request): # addNumber(model: ScheModel) transtion.regSchedule(model)
    req = await request.json()
    result = transaction.regSchedule(req)
    return result
    #str:phnNum

@callRouter.post("/delNumber",tags=["/call"])
async def delNumber(model: ScheduleManager): # addNumber(model: ScheModel) transtion.regSchedule(model)
    print("route")
    print(model.seq)
    print(model.__dict__)
    result = transaction.delSchedule(model)
    return JSONResponse(content=result)

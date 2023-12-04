import os
import json
import model
import transaction
import uvicorn
from database import engine
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.external import extRouter
from routers.server import serverRouter
from routers.call import callRouter
from routers.ws import wsRouter

from callListSchedule import PdsListSchedule
from klogging import *
from docs.tags import metadata

app = FastAPI(openapi_tags=metadata)

app.include_router(extRouter)
app.include_router(serverRouter)
app.include_router(callRouter)
# app.include_router(wsRouter)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/caller")
async def websocket_demo(websocket: WebSocket):
    await websocket.accept()
    while True: 
        data = await websocket.receive_text()
        
        print(data)

        await websocket.send_text(json.dumps(data))
            
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()

        serverStatus = transaction.recentScheStat()
        callList = transaction.readWaitingSchedule()

        result = {}
        result['serverStatus'] = serverStatus[0]
        result['callList'] = callList

        #info(result)

        await websocket.send_text(json.dumps(result))

@app.get("/")
async def root():
    return {"message": "Hello Q-PDS"}

# uvicorn
if __name__ == '__main__' :
    load_dotenv()
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run('app:app', host=os.getenv("HOST","127.0.0.1"), port=int(os.getenv("PORT",5064)), access_log=True,
                reload_dirs=['.'], reload=True
    )
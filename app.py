import json
import model
import transaction
from database import engine
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from callListSchedule import PdsListSchedule
from routers.external import extRouter
from routers.server import serverRouter
from routers.call import callRouter
from routers.ws import wsRouter
import uvicorn
from klogging import *

tags_metadata = [
    {
        "name": "/call",
        "description": "당일 기준 오토콜 목록을 리턴한다.",
    },
    {
        "name": "/api",
        "description": "음성모듈에서 INVITE 전화의 IN/OUT 구분을 확인하고 OUTBOUND콜인 경우 시나리오ID를 같이 리턴한다.",
        "externalDocs": {
            "description": "음성모듈",
            "url": "https://github.com/CheongbinKim/q-phone",
        },
    },
    {
         "name": "/server",
        "description": "PDS 서버 구동상태, 시작/중지 설정 API이다.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(extRouter)
app.include_router(serverRouter)
app.include_router(callRouter)
# app.include_router(wsRouter)

origins = [
    "*"
#    "http://localhost",
#    "http://localhost:9090",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run('app:app', host='0.0.0.0', port=9090, access_log=True,
                reload_dirs=['.'], reload=True
    )
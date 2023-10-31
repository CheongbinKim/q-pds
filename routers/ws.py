from fastapi import APIRouter,WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import transaction

wsRouter = APIRouter(prefix='/ws')

@wsRouter.websocket("/abc")
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
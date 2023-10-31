import time
import asyncio

import transaction
from autocall.callFunction import SendCall
from autocall.singleCall import SingleCall

from klogging import *

class MultiCall:
    def __init__(self):
        self.maxLineCount = 2
        self.currentRunnerCount = 0
        self.sender = SendCall(self.callback)
    
    async def run(self):
        while True:
            serverStatus = transaction.recentScheStat()
            
            if serverStatus[0]['stat'] == '0':
                info('서버가 실행 중이지 않습니다. 잠들어라...Zzz')
                await asyncio.sleep(1)
            else:
                if self.currentRunnerCount <= self.maxLineCount:
                    model = transaction.getScheduleForCall()

                    if model == None:
                        #info('오토콜 목록이 없습니다.')
                        await asyncio.sleep(1)
                    else:
                        self.currentRunnerCount = self.currentRunnerCount + 1
                        # DB상태변경 (연결중)
                        model["stat"] = "1"
                        transaction.updSchedule(model)
                        self.sender.setModel(model)
                        info("originate " + model["phnNum"])
                        self.sender.originate(model["phnNum"])
                else:
                    info('현재 남은 아웃바운드 회선이 없습니다...')
                    await asyncio.sleep(1)

    def callback(self):
        self.currentRunnerCount = self.currentRunnerCount - 1
        info("multiCall callback()")
        
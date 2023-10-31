import threading, requests, time
import transaction
from autocall.callFunction import SendCall
from klogging import *
import asyncio

class SingleCall:
    def __init__(self):
        self.isRun = False
        self.sender = SendCall(self.callback)
        self.flag = True

    def start(self):
        self.flag = True
        self.run()

    def stop(self):
        self.flag = False

    async def run(self):
        try:
            while True:
                serverStatus = transaction.recentScheStat()
                
                if serverStatus[0]['stat'] == '0':
                    info('서버가 실행 중이지 않습니다. 잠들어라...Zzz')
                    await asyncio.sleep(1)
                else:
                    if self.isRun == False:
                        model = transaction.getScheduleForCall()

                        if model == None:
                            #info('오토콜 목록이 없습니다.')
                            await asyncio.sleep(1)
                        else:
                            self.isRun = True
                            #print("originate 01064498979")
                            # DB상태변경 (연결중)
                            model["stat"] = "1"
                            transaction.updSchedule(model)
                            self.sender.setModel(model)
                            info("originate " + model["phnNum"])
                            self.sender.originate(model["phnNum"])
                    else:
                        #info("통화중이야..기다려!")
                        await asyncio.sleep(3)
        except KeyboardInterrupt:
            info("KeyboardInterrupt received")

    def callback(self):
        info("singleCall callback()")
        self.isRun = False




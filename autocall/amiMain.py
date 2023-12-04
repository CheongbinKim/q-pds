import transaction
from asterisk.ami import AMIClient
from klogging import *

class AmiMain:
    def __init__(self,callback):
        self.__client = AMIClient(address='223.130.135.113',port=5038,timeout=None)
        self.__client.login(username='admin',secret='amp1111')
        self.__client.add_event_listener(self.event_listener,white_list=['Hangup'])
    
    def run(self):
        # Single Mode / Multi Mode 확인
        pass

    def event_listener(self):
        if 'Exten' in event:
            connected_line_num = event['Exten']

            if connected_line_num == self.number:
                # 번호가 없어서 거절 된 케이스
                if 'Cause' in event:
                    if event['Cause'] == '21':  # Call Rejected
                        self.changeStat("5") # 없는 번호 상태
                    else:
                        self.changeStat("3")
                    self.callback()

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self,address,port,username,secret):
        


    
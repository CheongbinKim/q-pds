import transaction
from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
from asterisk.ami import EventListener
from klogging import *

class SendCall:
    def __init__(self,callback):
        self.client = AMIClient(address='223.130.135.113',port=5038,timeout=None)
        self.client.login(username='admin',secret='amp1111')
        self.client.add_event_listener(self.event_listener,white_list=['Hangup'])
        self.number = None
        self.callback = callback
        self.model = None

    def setModel(self,model):
        info("setModeL()")
        self.model = model
        info(self.model)

    def changeStat(self,stat):
        info("changeStat()")
        self.model['stat'] = stat                  # 연결성공
        info(self.model)
        transaction.updSchedule(self.model)

    def event_listener(self,event,**kwargs):
        
        info(event)
        if 'Exten' in event:
            info('Exten in!')
            info(type(event))
            try:
                info(event['Exten'])    
            except:
                info(event.Exten)
            connected_line_num = event['Exten']
            info(connected_line_num)
            if connected_line_num == self.number:
                info("Hangup")
                self.changeStat("3")
                self.callback()

    def callback_response(self,response):
        if response.status == 'Success':
            # DB 상태변경 (연결됨)
            info("connect")
            self.changeStat("2")
            
        else:
            # DB 상태변경 (연결실패)
            info("connect fail")
            self.changeStat("4")
            self.callback()

    def originate(self,number):
        self.number = number
        action = SimpleAction(
            'Originate',
            Channel='SIP/outgoing_07076630188/' + number,
            Exten=number,
            Priority=1,
            Context='qcontext',
            CallerID='python'
        )

        self.client.send_action(action,callback=self.callback_response)




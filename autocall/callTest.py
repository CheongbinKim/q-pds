# import time

# from asterisk.ami import AMIClient
# from asterisk.ami import SimpleAction
# from asterisk.ami import EventListener
# from asterisk.ami import Response

# def callback_response(response):
#     print('callback ',response)
#     print(response.status)
#     if response.status == 'Success':
#         print("연결 성공")
#     else:
#         print("연결 실패")
    

# def event_listener(event,**kwargs):
#     print(event)
#     if 'Exten' in event:
#         connected_line_num = event['Exten']
#         print(f'Exten: {connected_line_num}')
    

# client = AMIClient(address='223.130.135.113',port=5038,timeout=None)
# client.login(username='admin',secret='amp1111')
# client.add_event_listener(event_listener,white_list=['Hangup'])



# action = SimpleAction(
#     'Originate',
#     Channel='SIP/outgoing_07076630188/01064498979',
#     Exten='01064498979',
#     Priority=1,
#     Context='qcontext',
#     CallerID='python',
# )

# client.send_action(action,callback=callback_response)



# try:
#     while True:
#         time.sleep(10)
# except (KeyboardInterrupt, SystemExit):
#     client.logoff()

from singleCall import SingleCall

SingleCall()
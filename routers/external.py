from fastapi import Request, APIRouter
from databases import Database
import transaction

database = Database('sqlite:///scheduleManager.db')


from pydantic import BaseModel


class Item(BaseModel):
    number: str
    

extRouter = APIRouter(prefix='/api')

@extRouter.post("/isOut", tags=['/api'])
async def isOut(request: Request):
    req = await request.json()
    isOut = transaction.checkCallingNow(req['number'])
    return isOut
    #await database.connect()
    #query = '''
    #select 
    #case when exists 
    #(
    #select 1 
    #from scheduleManager 
    #where phnNum = '{0}' 
    #and stat in ('1','2')
    #and scheDt = date()
    #) then 'y' else 'n' end "result"
    #'''.format(number)
    #rows = await database.fetch_all(query=query)

    #await database.disconnect()

    #return rows[0]
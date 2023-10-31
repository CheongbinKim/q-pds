from alembic import Column, String, Integer, DateTime
from database import Base

class ScheduleList:
    
    
    sid (String, primary_key=True)
    scheDt= Column(DateTime, primary_key=True)
    phnNum (String, primary_key=True)
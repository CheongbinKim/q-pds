from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from database import Base

class ScheduleManager(Base):
    __tablename__ = "scheduleManager"
    __table_args__ = (
        UniqueConstraint('sid', 'scheDt', 'phnNum', name='scheduleManager_unique_commit'),
    )

    seq = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(String)
    scheDt= Column(String)
    phnNum= Column(String)
    stat= Column(String)
    regDt= Column(DateTime)
    updDt= Column(DateTime)

class ScheduleState(Base):
    __tablename__ = "scheduleState"

    seq= Column(Integer, primary_key=True, autoincrement=True)
    scheDttm= Column(String)
    stat= Column(String)
    regDt= Column(DateTime)


class ScheduleHistory(Base):
    __tablename__ = "scheduleHistory"
    __table_args__ = (
        UniqueConstraint('sid', 'scheDt', 'phnNum', name='scheduleHistory_unique_commit'),
    )

    seq= Column(Integer, primary_key=True, autoincrement=True)
    sid= Column(String)
    scheDt= Column(String)
    phnNum= Column(String)
    content= Column(String)
    regDt= Column(DateTime)
    

class CommCode(Base):
    __tablename__ = "commCode"

    codeGrp= Column(String, primary_key=True)
    codeGrpNm= Column(String)
    code= Column(String, primary_key=True)
    codeNm= Column(String)
    comment= Column(String)
    regDt= Column(DateTime)
    updDt= Column(DateTime)


class MaxLineCnt(Base):
    __tablename__ = "maxLineCnt"

    seq= Column(Integer, primary_key=True)
    cnt= Column(Integer)
    regDt= Column(DateTime)
    updDt= Column(DateTime)
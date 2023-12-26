import json

from database import Base
from database import sessionInfo
from datetime import datetime
from model import ScheduleManager
from model import ScheduleHistory
from model import ScheduleState
from model import CommCode
from model import MaxLineCnt
from sqlalchemy import func
from types import SimpleNamespace


conn = sessionInfo()

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


#Spring - Mybatis처럼...
# 스케줄 등록
# param Type : Model
def regSchedule(resource):
    try:
        rtnObj = Object()
        scheDt = datetime.now().strftime('%Y%m%d')
        print(scheDt)
        q = ScheduleManager(sid=resource['sid'], scheDt=scheDt, phnNum=resource['phnNum'], stat=0, regDt=datetime.now(), updDt=datetime.now())

        print(q)
        ''' 
        rtnObj.msg = ""
        if q > 0:
            rtnObj.msg = "추가되었습니다."
            rtnObj.rst = "success"
        else:
            rtnObj.msg = "추가된 내역이 존재하지 않습니다."
            rtnObj.rst = "error"
        '''
        conn.add(q)
        conn.commit()
        return rtnObj

    except:
        print("rollback")
        conn.rollback()


# 스케줄 상태 수정
# param Type : Model
def updSchedule(resource):
    try:
        print("updSchedule In")
        print(resource)
        if (resource["phnNum"]) == None:
            raise Exception("휴대폰 번호는 필수입니다.")
        print(resource["phnNum"])
        # if hasattr(resource, "seq") == False:
        #     print("if seq In")
        #     raise Exception("Seq는 필수입니다.")

        q = conn.query(ScheduleManager).filter(ScheduleManager.sid==resource["sid"], ScheduleManager.scheDt==resource["scheDt"], ScheduleManager.phnNum==resource["phnNum"], ScheduleManager.seq==resource["seq"]).update({'stat':resource["stat"], 'updDt':datetime.now()})
        conn.commit()

    except:
        conn.rollback()
        raise

# 스케줄 삭제
# param Type : json
def delSchedule(resource):
    try:
        '''
        if hasattr(resource, "phnNum") == False:
            raise Exception("휴대폰 번호는 필수입니다.")

        if hasattr(resource, "seq") == False:
            raise Exception("Seq는 필수입니다.")
        '''
        #print("delSchedule In")
        q = conn.query(ScheduleManager).filter(ScheduleManager.seq==resource.seq).delete()

        conn.commit()

    except:
        conn.rollback()

# 조건에 맞는 스케줄 조회
# param Type : Json
def readSchedule(resource):
    q = conn.query(ScheduleManager).filter(ScheduleManager.sid==resource.sid, ScheduleManager.scheDt==resource.scheDt, ScheduleManager.phnNum==resource.phnNum, ScheduleManager.seq==resource.seq, ScheduleManager.stat==resource.stat).all()
    return q

# 대기중인 스케쥴 조회
def readWaitingSchedule():
    scheDt = datetime.now().strftime('%Y%m%d')
    q = conn.query(ScheduleManager).filter(ScheduleManager.scheDt==scheDt).order_by(ScheduleManager.regDt.desc()).all()
    list = []
    for c in q:
        obj = Object()
        obj.seq = c.seq
        obj.sid = c.sid
        obj.scheDt = c.scheDt
        obj.stat = c.stat
        obj.phnNum = c.phnNum
        obj.updDt = c.updDt.strftime("%Y-%m-%d %H:%M:%S")
        list.append(obj.__dict__)

    # json.dumps(list)
    return list

# 전화를 걸기 위한 목록 가져오기
def getScheduleForCall():
    scheDt = datetime.now().strftime('%Y%m%d')
    q = conn.query(ScheduleManager).filter(ScheduleManager.scheDt==scheDt,ScheduleManager.stat=="0").order_by(ScheduleManager.scheDt.desc()).first()

    obj = Object()
    if q:
        obj.seq = q.seq
        obj.sid = q.sid
        obj.scheDt = q.scheDt
        obj.stat = q.stat
        obj.phnNum = q.phnNum

        '''
        callInfo = checkCallingNow(q.phnNum)
        print(callInfo)
        
        if callInfo:
            obj.isOut = callInfo["isOut"]

        print(obj.isOut)
        '''

        return obj.__dict__
    else:
        return None

    

# OutCall을 통한 전화인지 체크
# param Type : Str
def checkCallingNow(phnNum):
    q = conn.query(ScheduleManager).filter(ScheduleManager.stat=="1", ScheduleManager.phnNum==phnNum).all()

    obj = Object()
    for c in q:
        obj.sid = c.sid
        obj.phnNum = c.phnNum
        obj.isOut = True

    if hasattr(obj, "sid") == False:
        obj.sid = None
        obj.phnNum = None
        obj.isOut = False

    return obj.__dict__

# 스케줄러 데몬 상태 등록
# param Type : Json
def regScheStat(resource):
    try:
        print(resource)
        scheDt = datetime.now().strftime('%Y%m%d')
        q = ScheduleState(scheDttm=scheDt, stat=resource['stat'], regDt=datetime.now())
        conn.add(q)
        conn.commit()
    except:
        conn.rollback()

# 스케줄러 데몬 상태 조회
# param Type : Json
def readScheStat(resource):
    scheDt = resource.scheDt
    q = conn.query(ScheduleState.scheDttm, ScheduleState.stat, CommCode.codeNm).select_from(ScheduleState).join(CommCode, ScheduleState.stat == CommCode.code).filter(ScheduleState.scheDttm==scheDt,CommCode.codeGrp == "SCHESTAT").order_by(ScheduleState.scheDttm.desc()).all()
    return q

# 현재 스케줄러 데몬 상태 조회
def recentScheStat():
    scheDt = datetime.now().strftime('%Y%m%d')
    #q = conn.query(ScheduleState.scheDttm, ScheduleState.stat, CommCode.codeNm).select_from(ScheduleState).join(CommCode, ScheduleState.stat == CommCode.code).filter(ScheduleState.scheDttm==scheDt,CommCode.codeGrp == "SCHESTAT").order_by(ScheduleState.scheDttm.desc()).first()
    q = conn.query(ScheduleState).select_from(ScheduleState).join(CommCode, ScheduleState.stat == CommCode.code).filter(CommCode.codeGrp == "SCHESTAT").order_by(ScheduleState.regDt.desc()).first()

    list = []
    if q:
        list.append({ "stat" : q.stat })

    return list


# 스케줄 히스토리 등록
# param Type : Json
def regScheduleHist(resource):
    try:
        q = ScheduleHistory(sid=resource.sid, scheDt=resource.scheDt, phnNum=resource.phnNum, content=resource.content, regDt=datetime.now())
        conn.add(q)
        conn.commit()
    except:
        conn.rollback()

# 조건에 맞는 스케줄 히스토리 조회
# param Type : Json
def readScheduleHist(resource):
    q = conn.query(ScheduleHistory).filter(ScheduleHistory.sid==resource.sid, ScheduleHistory.scheDt==resource.scheDt, ScheduleHistory.phnNum==resource.phnNum, ScheduleHistory.seq==resource.seq).all()
    return q


def getMaxLineCnt():
    q = conn.query(MaxLineCnt).first()
    print(q)
    return q

def setMaxLineCnt(resource):
    
    q = conn.query(MaxLineCnt).filter(MaxLineCnt.seq==resource["seq"]).update({'cnt':resource["cnt"], 'updDt':datetime.now()})

    return q

def regMaxLineCnt(resource):
    print(resource)
    try:
        q = MaxLineCnt(seq=resource.seq, cnt=resource.cnt, regDt=datetime.now())
        conn.add(q)
        conn.commit()
    except:
        conn.rollback()
    #q = MaxLineCnt(seq=resource["seq"], cnt=resource["cnt"], regDt=datetime.now())
    return q

   
if __name__ == "__main__":

    #data = '{"sid": "1", "scheDt": "20231001", "phnNum":"01025764814", "stat":"0", "seq":"7"}'
    #data = '{"sid": "1", "scheDt": "20231001", "stat":"2", "phnNum":"01025764814"}'
    data = '{"cnt":"3", "seq":"1"}'
    #data = '{"phnNum":"01029209640", "scheDt":"20231021", "sid":"1", "seq":"2", "stat":"1"}'
    #data = '{"phnNum":"01029209640", "scheDt":"20231021", "sid":"1", "seq":"2"}'
    #data = '{"phnNum":"01029209640", "sid":"1"}'
    #data = {"stat":"1"}

    # Parse JSON into an object with attributes corresponding to dict keys.
    x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    #날짜 YYYY-MM-DD로 변환 시작
    #print(datetime.now().strftime('%Y-%m-%d'))
    #날짜 YYYY-MM-DD로 변환 끝

    #regSchedule(x)
    #updSchedule(x)
    #readWaitingSchedule()
    #readSchedule()
    #delSchedule(x)
    #readWaitingSchedules()
    #recentScheStat()
    #regScheStat(data);
    #checkCallingNow("01029209640")
    #dataCall = getScheduleForCall()
    #dataCall["stat"] = "1"
    #jsonObj = json.dumps(dataCall)
    #print(dataCall)
    #updSchedule(dataCall)

    regMaxLineCnt(x)


    # JSON Parsing Complete .. 데이터를 어떻게 받을 지 확인이 필요함.

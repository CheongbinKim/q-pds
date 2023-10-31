
import schedule
import time


class PdsListSchedule:
    def __init__(self):
        self.job = schedule.every(1).seconds.do(self.jobTask)
        self.runSchedule()

    def runSchedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def jobTask(self):
        print("Call List 가져오기")

    def startJob(self):
        self.job = schedule.every(1).seconds.do(self.jobTask)

    def cancelJob(self):
        schedule.cancel_job(self.job)
        
        


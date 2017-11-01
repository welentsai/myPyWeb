# from system library
import datetime
import schedule
import time

# user-defined module
from webCrawlers import bot_day_rate
from webCrawlers import monitor_air
from mDbLib import mLab_Conn
from mDbLib import taskDb

count = 0

def job():
	global count # explict declare to refer to global variable 'count'
	print("I'm counting..." + str(count))
	count += 1
	# print(datetime.date.today())

# 從台銀網站取得每日匯率資料
def job_getExRate():
	print('Task!! getExRate()')
	rateList = bot_day_rate.getTwExRateList()
	strRateList = [str(rate) for rate in rateList] # convert tuple list to string list
	newTask = taskDb.TaskRec(Date=datetime.date.today(), Op='exRate', Dur='day', Raw=strRateList)
	newTask.save()
	# bot_day_rate.display(rateList)

def job_getPM25():
	pm25List = monitor_air.getPM25()
	monitor_air.display(pm25List)

# schedule.every(60).seconds.do(job)
# schedule.every(30).minutes.do(job_getExRate)
# schedule.every(20).minutes.do(job_getPM25)
# schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

if __name__ == "__main__":
	myConn = mLab_Conn.MyConn() # connect to mLab DB
	# schedule.every(5).seconds.do(job_getExRate)
	schedule.every().day.at("18:00").do(job_getExRate)
	# schedule.every(2).seconds.do(job_getPM25)

	while True:
		schedule.run_pending() # Run all jobs that are scheduled to run
		time.sleep(1) # Suspend execution in seconds

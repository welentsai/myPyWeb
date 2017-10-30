import schedule
import time

from webCrawlers import bot_day_rate

count = 0

def job():
	global count # explict declare to refer to global variable 'count'
	print("I'm counting..." + str(count))
	count += 1

# 從台銀網站取得每日匯率資料
def job_getExRate():
	rateList = bot_day_rate.getTwExRateList()
	bot_day_rate.display(rateList)

schedule.every(10).seconds.do(job)
schedule.every(30).seconds.do(job_getExRate)
# schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
	schedule.run_pending() # Run all jobs that are scheduled to run
	time.sleep(10) # Suspend execution in seconds
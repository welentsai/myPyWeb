# from system library
import datetime
import schedule
import time

# user-defined module
from webCrawlers import bot_day_rate
from webCrawlers import monitor_air
from webCrawlers import sp500Spider
from mDbLib import mLab_Conn
from mDbLib import taskDb
from mDbLib import sp500Db

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
	newTask = taskDb.TaskRec(Date=datetime.datetime.today(), Op='exRate', Dur='day', Status='new', Raw=strRateList)
	print(newTask)
	newTask.save()

# 取得 台灣各地PM2.5的監測資料
def job_getPM25():
	print('Task!! getPM25()')
	pm25List = monitor_air.getPM25()
	strPm25List = [str(pm25) for pm25 in pm25List] # convert tuple list to string list
	newTask = taskDb.TaskRec(Date=datetime.datetime.today(), Op='pm25', Dur='day', Status='new', Raw=strPm25List)
	print(newTask)

# 更新每日SP500交易資料
def job_updateSP500Tradings():
	print('Task!! updateSP500Tradings()')
	lastDt = sp500Db.SP500.objects.order_by('-Date').first().Date # 取得最後一筆交易資料
	# lastDt = '2017-10-25'
	year = datetime.datetime.today().year # 今年
	df = sp500Spider.getData(str(year), '10') # 取得今年最後10筆交易
	df = df.set_index(['Date']) 
	# df.loc[:end_idx] => get data from first to end_idx
	df = df.loc[:lastDt] # get data from first to last date
	df =  df.drop(df.index[len(df)-1]) # drop last row (already in db)
	df = df.reset_index() # reset to auto index
	if(len(df)):
		print('new SP500 tradings !!')
		tradings = []
		for idx, row in df.iterrows():
			# create new SP500 document
			trading = sp500Db.SP500(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low, Close=row.Close, Volume=row.Volume)
			# print(trading)
			tradings.append(trading)
		# print("tradings count : " + str(len(tradings)))
		print(tradings)
		sp500Db.SP500.objects.insert(tradings)
	else:
		print('No New SP500 Trading Data !!')
	
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
	# schedule.every(5).seconds.do(job_getPM25)
	schedule.every().day.at("18:00").do(job_getExRate) 
	schedule.every().day.at("10:00").do(job_updateSP500Tradings)

	while True:
		schedule.run_pending() # Run all jobs that are scheduled to run
		time.sleep(1) # Suspend execution in seconds

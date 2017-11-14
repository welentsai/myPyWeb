# -*- coding: utf-8 -*-

# from system library
import datetime
import schedule
import time

# user-defined module
from webCrawlers import bot_day_rate
from webCrawlers import monitor_air
from webCrawlers import sp500Spider
from webCrawlers import tw0050Spider
from webCrawlers import tw0050Holdings_Spider
from webCrawlers import fedRateSpider
from mDbLib import mLab_Conn
from mDbLib import taskDb
from mDbLib import sp500Db
from mDbLib import tw0050Db
from mDbLib import tw0050Holdings_Db
from mDbLib import fedEFFR_Db

count = 0

def job():
	global count # explict declare to refer to global variable 'count'
	print("I'm counting..." + str(count))
	count += 1
	# print(datetime.date.today())

# 從台銀網站取得每日匯率資料
def job_getExRate():
	print('Task!! getExRate()')
	print(datetime.datetime.today())
	rateList = bot_day_rate.getTwExRateList()
	strRateList = [str(rate) for rate in rateList] # convert tuple list to string list
	newTask = taskDb.TaskRec(Date=datetime.datetime.today(), Op='exRate', Dur='day', Status='new', Raw=strRateList)
	print(newTask)
	newTask.save()

# 取得 台灣各地PM2.5的監測資料
def job_getPM25():
	print('Task!! getPM25()')
	print(datetime.datetime.today())
	pm25List = monitor_air.getPM25()
	strPm25List = [str(pm25) for pm25 in pm25List] # convert tuple list to string list
	newTask = taskDb.TaskRec(Date=datetime.datetime.today(), Op='pm25', Dur='day', Status='new', Raw=strPm25List)
	print(newTask)

# 更新每日SP500交易資料
def job_updateSP500Tradings():
	print('Task!! updateSP500Tradings()')
	print(datetime.datetime.today())
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

# 更新每日TW50交易資料
def job_updateTW0050Tradings():
	print('Task!! updateTW0050Tradings()')
	today = datetime.datetime.today()
	df = tw0050Spider.getData(today.year, today.month, '0050') # 當月交易資料
	df = df.set_index(['Date'])
	lastDt = tw0050Db.Tw0050.objects.order_by('-Date').first().Date # 取得DB最後一筆交易資料
	# lastDt = '2017-11-01'
	print('last record date in db => ' + str(lastDt))
	# print(df)
	df = df.loc[lastDt:] # get the rest data from last date
	df =  df.drop(df.index[0]) # drop first row (already in db)
	df = df.reset_index() # reset to auto index
	# print(df)
	if(len(df)):
			# print('new tradings')
			tradings = []
			for idx, row in df.iterrows():
				# create new Tw0050 document
				trading = tw0050Db.Tw0050(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low,
																	Close=row.Close, Volume=row.Volume, Turnover=row.Turnover)
				# print(trading)
				tradings.append(trading)
			print("New tradings count : " + str(len(tradings)))
			print(tradings)
			tw0050Db.Tw0050.objects.insert(tradings)
	else:
		print('No New Data !!')

# 更新每季TW50持股資訊
def job_updateTW0050Holdings():
	print('Task!! job_updateTW0050Holdings()')

	lastYr = tw0050Holdings_Db.Tw0050Holding.objects.order_by('-Year').first().Year # 取得最後一筆交易年份
	lastQtr = tw0050Holdings_Db.Tw0050Holding.objects(Year=lastYr).order_by('-Quarter').first().Quarter # 取得最後一筆交易季度
	lastDTuple = (int(lastYr), int(lastQtr))

	today = datetime.date.today()
	prev_quarter_map = ((1, 0), (2, 0), (3, 0), (4, 0))
	quarter, yd = prev_quarter_map[(today.month - 1) // 3] # 整數除法, 以[0~11] map to [0~3]的結果
	todayTuple = (today.year + yd, quarter)

	if todayTuple > lastDTuple: # 新季度
		print('Neq Quarter !!  Try to update if data is ready ...')
		df = tw0050Holdings_Spider.getData(todayTuple[0], todayTuple[1])
		if df == None:
			print('None Data !!')
			return None # early Return
		if(len(df)):
			# print('new tradings')
			holdings = []
			for idx, row in df.iterrows():
				# create new Tw0050 holding document
				holding = tw0050Holdings_Db.Tw0050Holding(Year=row.Year, Quarter=row.Quarter, Code=row.Code, Name=row.Name, Ratio=row.Ratio)
				# print(holding)
				holdings.append(holding)
			print("New Holdings count : " + str(len(holdings)))
			tw0050Holdings_Db.Tw0050Holding.objects.insert(holdings)
		else:
			print('No New Data !!')
	else:
		print("Not a New Quarter !!")

# 更新每日Fed Fund Rate資訊
def job_updateFedRates():
	print('Task!! job_updateFedRates()')
	startDate = fedEFFR_Db.FedRate.objects.order_by('-Date').first().Date # 取得最後一筆資料的日期
	endDate = datetime.date.today()
	print(startDate)
	print(endDate)
	df = fedRateSpider.getData(startDate, endDate)
	df =  df.drop(df.index[len(df)-1]) # drop last row, startDate, (already in db)
	if(len(df)):
		rates = []
		for idx, row in df.iterrows():
			rate = fedEFFR_Db.FedRate(Date=row.Date, Rate=row.Rate)
			rates.append(rate)
		print("New rates count : " + str(len(rates)))
		# print(rates)
		fedEFFR_Db.FedRate.objects.insert(rates)
	else:
		print('No New Data !!')
	
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
	# schedule.every(5).seconds.do(job_updateFedRates)
	schedule.every().day.at("18:00").do(job_getExRate) # 台幣匯率
	schedule.every().day.at("18:30").do(job_updateTW0050Tradings) # TW0050
	schedule.every().day.at("10:00").do(job_updateSP500Tradings) # SP500
	schedule.every().day.at("10:10").do(job_updateFedRates)  # Fed Rate
	schedule.every(30).days.at("19:00").do(job_updateTW0050Holdings) # once in 30 days

	while True:
		schedule.run_pending() # Run all jobs that are scheduled to run
		time.sleep(60) # Suspend execution in seconds

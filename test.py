# -*- coding: utf-8 -*-
import pandas as pd

from webCrawlers import sp500

# main program entry
if __name__ == "__main__":
	df = sp500.getData(str('2016'))
	df.sort_values(by=['Date'])
	print(df.sort_values(by=['Date']))

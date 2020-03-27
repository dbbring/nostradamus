#! /usr/bin/env python

import sys
from datetime import date, datetime

from data_operations.utils.scrapers import *
from data_operations.utils.api_requests import *
from data_operations.database.helpers import *
from shared.models import Ticker
# ============== TODO =========================

# Figure out a way to move the date objects out of news
# maybe we need to store off price from finvix and compare to api call to make sure we are getting the right ticker

# keep in mind this for the current day of gaining 10%. We need the previous days because the current means nothing to us.

# also store off sub sector for future data anaysis but get top level sector to compare gains


# use trendln package to get support and resistance points https://github.com/GregoryMorse/trendln




index = 1
end_id = 1
end_of_list = False
tickers = ['mcf']


# Fetch all the tickers the meets our criteria
while not end_of_list:
  FV = FinViz('../nostradamus_files/finviz-r=' + str(index) + '.html')
  pg_tickers = FV.get_tickers(25, 4.8)
  last_id = FV.get_last_finviz_row_id()
  if (end_id != last_id):
    index += 20
    end_id = last_id
    tickers += pg_tickers
  else:
    end_of_list = True



for ticker in tickers:
  FV = FinViz('../nostradamus_files/finviz=' + ticker + '.html')
  if (FV.has_finviz_news()):
    tickers.remove(ticker)
  else:
    TD = TDAmeritrade(ticker)
    if not TD.has_td_news():
      # try catch here and just pass dont save information if exception
      company = Ticker()
      company.basic_info.data['ticker'] = ticker
      company.basic_info.data['date'] = datetime.now().date()
      company.basic_info.data['percent_change'] = TD.get_percent_change()
      # get sector name and subname and shorties and tute ownership then proceed on

      # Check IEX for News
      # All green lights grab information from alpha vantage and start processing


# send mail with entire ticker list
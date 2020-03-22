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
# check date on fundmental (fin model prep api) some are wicked out of date, maybe hit another source?

# keep in mind this for the current day of gaining 10%. We need the previous days because the current means nothing to us.




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
      company = Ticker()
      company.basic_info.data['ticker'] = ticker
      company.basic_info.data['date'] = datetime.now().date()
      company.basic_info.data['percent_change'] = TD.get_percent_change()



# when saving, just call save on each model if its an array
# send mail with entire ticker list
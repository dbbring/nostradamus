#! /usr/bin/env python

import sys
from datetime import date, datetime, timedelta

from data_operations.utils.scrapers import FinViz, TDAmeritrade
from data_operations.utils.api_requests import AlphaVantage, IEX
from data_operations.database.helpers import DB
from shared.models import Ticker
# ============== TODO =========================

# Figure out a way to move the date objects out of news

# maybe we need to store off price from finvix and compare to api call to make sure we are getting the right ticker

# =========== Init ==========================
db = DB()
tickers = ['mcf']
sp = AlphaVantage('.ixc')
sp_inputs = sp.get_inputs()

# ========== Get a list of tickers ============
finviz_pg_index = 1
end_id = 1
end_of_list = False
'''
# Fetch all the tickers the meets our criteria
while not end_of_list:
  FV = FinViz('../nostradamus_files/finviz-r=' + str(finviz_pg_index) + '.html')
  pg_tickers = FV.get_tickers(25, 4.8)
  last_id = FV.get_last_finviz_row_id()
  if (end_id != last_id):
    finviz_pg_index += 20
    end_id = last_id
    tickers += pg_tickers
  else:
    end_of_list = True
'''
# =========== Process List of tickers =============
for ticker in tickers:
  FV = FinViz('../nostradamus_files/finviz=' + ticker + '.html')
  if (FV.has_finviz_news()):
    tickers.remove(ticker)
  else:
    TD = TDAmeritrade(ticker)
    if not TD.has_td_news():
      # try catch here and just pass dont save information if exception
      # sleep for 15 secs here and  then spin off new thread
      company = Ticker()
      company.basic_info.data['ticker'] = ticker
      #company.basic_info.data['date'] = datetime.now().date()
      company.basic_info.data['date'] = datetime.today() - timedelta(days=7) 
      company.basic_info.data['percent_change'] = TD.get_percent_change()
      sectors = TD.get_sector()

      symbol = AlphaVantage(ticker)
      symbol_wk = AlphaVantage(ticker, False)
      inputs = symbol.get_inputs()
      wk_inputs = symbol_wk.get_inputs()
      inputs['s_p'] = sp_inputs['close']

      # stop each array after x number of days we dont need the whole thing
      # these two numbers also effect how many days we gather tracking information
      start = len(inputs['date']) - 1
      end = start - 5
      
      for index in range(start, end, -1):
        wk_data = symbol_wk.make_price_wk_model(wk_inputs, index)
        company.weekly.append(wk_data)

        eod_data = symbol.make_price_eod_model(inputs, index)
        company.eod.append(eod_data)

        tech_data = symbol.make_tech_indic_model(inputs, index)
        company.tech_anaylsis.append(tech_data)

        chart_data = symbol.make_chart_idic_model(inputs, index)
        company.chart_anaylsis.append(chart_data)

      fa = IEX(ticker)
      fa_data = fa.make_fund_indic_model(inputs)
      fa.data['sector'] = sectors['top-level']
      fa.data['sub_sector'] = sectors['second-level']
      fa.data['institutional_ownership'] = TD.get_tute_ownership()
      fa.data['short_interest_percent'] = TD.get_short_intrest()

      company.fund_anaylsis = fa_data

      # if whatever reason we fail, dont bother saving
      db.save_ticker_model(company)

# =============== Update old tickers (Price EOD only) =====
tickers_need_updated = db.select_tracking_tickers()

for ticker_info in tickers_need_updated:
  # Sleep for 15 secs here for Alphavantage buffer
  tran_id, ticker = ticker_info
  symbol = AlphaVantage(ticker)
  inputs = symbol.get_inputs()

  start = len(inputs['date']) - 1
  end = start - 5

  for index in range(start, end, -1):
    eod_data = symbol.make_price_eod_model(inputs, index, is_tracking=True)
    eod_data.data['transaction_id'] = tran_id
    db.save(eod_data)


# send mail with entire ticker list

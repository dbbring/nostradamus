#! /usr/bin/env python
# ======================= Gen Imports ========================
from datetime import date, datetime, timedelta
from multiprocessing import Process
import sys
from time import sleep

# ====================== Custom Imports ======================
from data_operations.utils.helpers import send_mail, process_ticker
from data_operations.utils.scrapers import FinViz, TDAmeritrade
from data_operations.utils.api_requests import AlphaVantage
from data_operations.database.helpers import DB



# ===============================================================
#                     Init 
# ===============================================================
msg = '-- Main Nostradamus Script Successful!! -- \n\n ' +  'Tickers added are: \n\n'
tickers = ['mcf']

try:
  sp = AlphaVantage('.INX')
  sp_inputs = sp.get_inputs()
  # =============================================================
  #                 Get a list of tickers 
  # =============================================================
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
  # =============================================================
  #                  Process List of tickers
  # =============================================================

  for ticker in tickers:
    FV = FinViz('../nostradamus_files/finviz=' + ticker + '.html')
    if (FV.has_finviz_news()):
      tickers.remove(ticker)
    else:
      TD = TDAmeritrade(ticker)
      if not TD.has_td_news():
        msg += ticker + '\n'
        #sleep(30)   # Rate Limiting for Alphavantage
        new_thread = Process(target=process_ticker, args=(TD, ticker, sp_inputs))
        new_thread.start() 
except Exception as err:
  send_mail('-- Main Nostradamus Code Block Failed!! -- \n\n ' + err)


# ===============================================================
#                 Update old tickers (Price EOD only) 
# ===============================================================

db = DB()
tickers_need_updated = db.select_tracking_tickers()
msg += '\n --- Updated Tracking Prices on: \n\n'

for ticker_info in tickers_need_updated:
  try:
    # 60 delay for Rate Limiting on Alphavantage
    #sleep(60)
    tran_id, ticker = ticker_info
    symbol = AlphaVantage(ticker)
    inputs = symbol.get_inputs()

    start = len(inputs['date']) - 1
    end = start - 5

    for index in range(start, end, -1):
      eod_data = symbol.make_price_eod_model(inputs, index, is_tracking=True)
      eod_data.data['transaction_id'] = tran_id
      db.save(eod_data)

    msg += ticker + '\n'
  except Exception as err:
    send_mail('-- Updating Tracking Tickers Code Block Failed!! -- \n\n ' + err)

send_mail(msg)

#! /usr/bin/env python
# ======================= Gen Imports ========================
from datetime import date, datetime, timedelta
from multiprocessing import Process
import sys
from time import sleep
import json
import traceback
import sys

# ==== Add our path to the python path so we can import our modules ====
with open('./data_operations/config.json') as f:
            config = json.load(f)

sys.path.insert(1, config['project_root'])

# ====================== Custom Imports ======================
from data_operations.utils.util import send_mail, process_ticker
from data_operations.utils.helpers import FireFox
from data_operations.utils.scrapers import FinViz, TDAmeritrade
from data_operations.utils.api_requests import AlphaVantage
from data_operations.database.helpers import DB


# ===============================================================
#                     Init 
# ===============================================================

try:
  browser = FireFox()
  browser.config = config
  sp = AlphaVantage('.INX')
  sp_inputs = sp.get_inputs()
  for data_item in config['nostradamus']:
    msg = '--- Results From '+ data_item['database_name'] +' --- \n\n ' +  '-- Tickers added are: \n\n'

    # =============================================================
    #                 Get a list of tickers 
    # =============================================================
    finviz_pg_index = 1
    end_id = 1
    end_of_list = False
    ticker_count = 0
    tickers = []
    # Fetch all the tickers the meets our criteria
    while not end_of_list:
      FV = FinViz((data_item['screener_url'] + str(finviz_pg_index)), browser)
      pg_tickers = FV.get_tickers(data_item['upper_bound'], data_item['lower_bound'])
      last_id = FV.get_last_finviz_row_id()
      if (end_id != last_id):
        finviz_pg_index += 20
        end_id = last_id
        tickers += pg_tickers
      else:
        end_of_list = True
    

    # =============================================================
    #                  Process List of tickers
    # =============================================================

    for ticker in tickers:
      try:
        FV = FinViz('https://finviz.com/quote.ashx?t=' + ticker, browser)
        if (FV.has_finviz_news()):
          tickers.remove(ticker)
        else:
          TD = TDAmeritrade(ticker)
          if not TD.has_td_news() and ticker_count < data_item['num_of_tickers_to_process']:
            ticker_count += 1
            msg += '---- ' + ticker + '\n'
            sleep(30)   # Rate Limiting for Alphavantage
            new_thread = Process(target=process_ticker, args=(data_item['database_name'], TD, FV, ticker, sp_inputs))
            new_thread.start() 

            if ticker_count == data_item['num_of_tickers_to_process']:
              break  # We have all the data we need, stop parsing

      except Exception as err:
        error_msg = traceback.format_exc()
        send_mail('-- Couldnt Add Ticker '+ ticker +' -- \n\n ' + str(repr(err)) + '\n\n' + error_msg, data_item['database_name'])

    # ===============================================================
    #                 Update old tickers (Price EOD only) 
    # ===============================================================

    if data_item['update_tickers']:
      db = DB(data_item['database_name'])
      tickers_need_updated = db.select_tracking_tickers()
      msg += '\n -- Updated Tracking Prices on: \n\n'

      for ticker_info in tickers_need_updated:
        try:
          # 60 delay for Rate Limiting on Alphavantage
          sleep(60)
          tran_id, tran_ticker = ticker_info
          symbol = AlphaVantage(tran_ticker)
          inputs = symbol.get_inputs()

          start = len(inputs['date']) - 1
          end = start - 5

          for index in range(start, end, -1):
            eod_data = symbol.make_price_eod_model(inputs, index, is_tracking=True)
            eod_data.data['transaction_id'] = tran_id
            db.save(eod_data)

          msg += tran_ticker + '\n'
        except Exception as err:
          error_msg = traceback.format_exc()
          send_mail('-- Updating Tracking Tickers Code Block Failed!! -- \n\n ' + str(repr(err) + '\n\n' + error_msg), data_item['database_name'])

    # Finished with everything (Succesfull or not), send off email notification
    msg += '\n\n**There is not guarentee that all the tickers have been succesfully processed and saved. Please Check the DB to verify..'
    send_mail(msg, data_item['database_name'])

except Exception as err:
  error_msg = traceback.format_exc()
  send_mail('-- Main Nostradamus Code Block Failed!! -- \n\n ' + str(repr(err)) + '\n\n' + error_msg, data_item['database_name'])
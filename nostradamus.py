#! /usr/bin/env python
# ======================= Gen Imports ========================
import argparse
from datetime import date, datetime, timedelta
from multiprocessing import Process
import sys
from time import sleep

# ====================== Custom Imports ======================
from data_operations.utils.helpers import send_mail, process_ticker
from data_operations.utils.scrapers import FinViz, TDAmeritrade
from data_operations.utils.api_requests import AlphaVantage
from data_operations.database.helpers import DB

# ======== TODO ======
# add geoprahpicaly local companys table
# add same sector company table
# limit to 20 tickers for gains and 20 for losers per day?
# comp by sector table using price eod model use yfinance
# comp by physical location using price eod model


# ===============================================================
#                     Init 
# ===============================================================
args_setup = argparse.ArgumentParser(description='Main Entry Script for Populating DB')
args_setup.add_argument('db_name', metavar='Database_Name', type=str, help="Which database instance to use")
args_setup.add_argument('upper_bound', metavar='Screener_Upper_Bound', type=float, help="The upper bound in which the screener will look for.")
args_setup.add_argument('lower_bound', metavar='Lower_Upper_Bound', type=float, help="The lower bound in which the screener will look for.")

msg = '--- Main Nostradamus Script Finished!! --- \n\n ' +  '-- Tickers added are: \n\n'
tickers = ['mcf']
args = args_setup.parse_args()

#try:
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
  FV = FinViz('https://finviz.com/screener.ashx?v=111&f=ind_stocksonly,sh_avgvol_o300,ta_perf_dup&ft=4&o=-change&r=' + str(finviz_pg_index))
  pg_tickers = FV.get_tickers(args.upper_bound, args.lower_bound)
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
  # FV = FinViz('https://finviz.com/quote.ashx?t=' + ticker)
  FV = FinViz('../nostradamus_files/finviz=' + ticker + '.html')
  if (FV.has_finviz_news()):
    tickers.remove(ticker)
  else:
    TD = TDAmeritrade(ticker)
    if not TD.has_td_news():
      msg += '---- ' + ticker + '\n'
      #sleep(30)   # Rate Limiting for Alphavantage
      new_thread = Process(target=process_ticker, args=(args.db_name, TD,
      FV, ticker, sp_inputs))
      new_thread.start() 
#except Exception as err:
  #send_mail('-- Main Nostradamus Code Block Failed!! -- \n\n ' + str(repr(err)))
 # print(repr(err))


# ===============================================================
#                 Update old tickers (Price EOD only) 
# ===============================================================

db = DB(args.db_name)
tickers_need_updated = db.select_tracking_tickers()
msg += '\n -- Updated Tracking Prices on: \n\n'

for ticker_info in tickers_need_updated:
  try:
    # 60 delay for Rate Limiting on Alphavantage
    sleep(60)
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
    send_mail('-- Updating Tracking Tickers Code Block Failed!! -- \n\n ' + str(repr(err)))

send_mail(msg)

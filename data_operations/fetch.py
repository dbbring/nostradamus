import sys
from utils.scrapers import *
from utils.api_requests import *
# ============== TODO =========================
# Not thrilled about how we have to create a ton of new objects in FinViz
# Figure out a way to move the date objects out of news
# on bloomberg, do we strip all whitespace? eg healthcare or health care
# bb = Bloomberg()
# print(bb.get_sector_performance('health care'))
# maybe we need to store off price from finvix and compare to api call to make sure we are getting the right ticker
# check date on fundmental (fin model prep api) some are wicked out of date, maybe hit another source?


index = 1
end_id = 1
end_of_list = False
tickers = ['mcf']

'''
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
    # do we create a ticker object that can hold all our data while we process?
    # proceed to check TD and if has news, then pop out otherwise lets go on and start
    # grabbing data

    td = TDAmeritrade('mcf')

av = AlphaVantage('mcf')
'''



#===================================================================================
'''
if (len(sys.argv) > 1):
  bb = Bloomberg()
  print(bb.sectors)
'''  
#====================================================================================
import data_operations.utils.helpers as util
import requests


 # ======================================================= # 
 #            AlphaVantage API Calls                       #
 # ======================================================= #

# We can add more API keys to the array and cycle them if we start hitting out limit. 
# But they still block via IP. We will have use liquidVPN and enable the IP 
# modulation if we want to use mulitple API tokens. API returns a note if you 
# exceed the limit.

class AlphaVantage(util.API_Request):

    def __init__(self, ticker):
        self.base = super()
        self.ticker = ticker
        self.api_keys = ['KBE1FWN6A9NDD5JR', 'F0JH3005KCFVO1U9']
        self.api_key_counter = 0
        self.data = self.try_api_call(ticker)
        return


    def get_eod_data(self):
        # use our eod_table model here and go back how many days?
        return


    def try_api_call(self, ticker: str) -> dict:
        time.sleep(30)
        r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=' + self.api_keys[self.api_key_counter])
        res = r.json()
        if 'note' in res:
            return {}
        return res['Time Series (Daily)']
        

 # ======================================================= # 
 #            Financial Modeling Prep API Calls            #
 # ======================================================= #


class Fin_Mod_Prep(util.API_Request):

    def __init__(self):
        self.base = super()
        return


    def get_indices(self):
        r = requests.get('https://financialmodelingprep.com/api/v3/majors-indexes')
        res = r.json()
        return res['majorIndexesList']

 # ======================================================= # 
 #            IEX API Calls                                #
 # ======================================================= #


class IEX(util.API_Request):

    def __init__(self, ticker):
        # scrape here, singleton class, and maintain state of array of arrays %gains
        self.base = super()
        self.ticker = ticker
        return

    def get_sector_performance(sector):
        # 
        return
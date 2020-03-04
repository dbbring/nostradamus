from utils.helpers import * as util


 # ======================================================= # 
 #            AlphaVantage API Calls                       #
 # ======================================================= #


class AlphaVantage(util.API_Request):

    def __init__(self, ticker):
        # scrape here, singleton class, and maintain state of array of arrays %gains
        self.base = super()
        self.ticker = ticker
        return

    def get_sector_performance(sector):
        # 
        return
        

 # ======================================================= # 
 #            Financial Modeling Prep API Calls            #
 # ======================================================= #


class Fin_Mod_Prep(util.API_Request):

    def __init__(self, ticker):
        # scrape here, singleton class, and maintain state of array of arrays %gains
        self.base = super()
        self.ticker = ticker
        return

    def get_sector_performance(sector):
        # 
        return
        

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
import data_operations.utils.helpers as util
from shared.base_model import Base_Model
from shared.models import Chart_Indicators, Price_EOD, Price_Weekly, Technical_Indicators, Fundamental_Indicators

import requests
import time
import json
import numpy as np
from collections import OrderedDict
import talib


 # ======================================================= # 
 #            AlphaVantage API Calls                       #
 # ======================================================= #

class AlphaVantage(util.API_Request):

    def __init__(self, ticker: str, is_daily=True):
        self.base = super()
        self.ticker = ticker
        self.total_lookback_days = 55 # farthest right now is 50 for avg volume to start our anaylasis
        self.api_key = 'KBE1FWN6A9NDD5JR'
        #self.data = self.try_api_call(is_daily)
        if (is_daily):
            with open('./mcf.json') as f:
                self.data = json.load(f)
        else:
            with open('./mcf_weekly.json') as f:
                self.data = json.load(f)
        self.data = self.data['Time Series (Daily)'] if is_daily else self.data['Weekly Time Series']
        return


    def try_api_call(self, is_daily = True) -> dict:
        time.sleep(15)
        if (is_daily):
            r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + self.ticker + '&apikey=' + self.api_key)
            res = r.json()
        else:
            r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + self.ticker + '&apikey=' + self.api_key)
            res = r.json()
        if 'note' in res:
            return {}
        return res['Time Series (Daily)'] if is_daily else res['Weekly Time Series']


    def get_inputs(self) -> dict:
        current_period = 0 # count today for calculations but dont save it
        date_data = []
        percent_change_data = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []
        volume_data = []
        inputs = OrderedDict()

        for day in self.data:
            if current_period <= self.total_lookback_days:
                eod_data = []
                date_data.append(day)
                percent_change_data.append(Base_Model.to_percent(self, float(self.data[day]['1. open']), float(self.data[day]['4. close'])))
                open_data.append(float(self.data[day]['1. open']))
                high_data.append(float(self.data[day]['2. high']))
                low_data.append(float(self.data[day]['3. low']))
                close_data.append(float(self.data[day]['4. close']))
                volume_data.append(float(self.data[day]['5. volume']))
            current_period += 1

        # [::-1] Reverses array 
        inputs['open'] = np.array(open_data[::-1])
        inputs['high'] = np.array(high_data[::-1])
        inputs['low'] = np.array(low_data[::-1])
        inputs['close'] = np.array(close_data[::-1])
        inputs['volume'] = np.array(volume_data[::-1])
        inputs['date'] = date_data[::-1]
        inputs['percent_change'] = percent_change_data[::-1]

        inputs['avg_volume'] = talib.SMA(inputs['volume'], timeperiod=50)

        return inputs


    def make_price_eod_model(self, inputs: dict, index: int) -> Price_EOD:
        # Class factory to generate each price eod's 
        eod_model = Price_EOD()

        eod_model.data['date'] = inputs['date'][index]
        eod_model.data['open'] = inputs['open'][index]
        eod_model.data['high'] = inputs['high'][index]
        eod_model.data['low'] = inputs['low'][index]
        eod_model.data['close'] = inputs['close'][index]
        eod_model.data['volume'] = inputs['volume'][index]
        eod_model.data['avg_volume'] = inputs['avg_volume'][index]
        eod_model.data['percent_change'] = inputs['percent_change'][index]
        eod_model.data['is_tracking_period'] = False

        return eod_model


    def make_price_wk_model(self, inputs: dict, index: int) -> Price_Weekly:
        wk_model = Price_Weekly()

        wk_model.data['wk_start_date'] = inputs['date'][index - 1]
        wk_model.data['wk_end_date'] = inputs['date'][index]
        wk_model.data['open'] = inputs['open'][index]
        wk_model.data['high'] = inputs['high'][index]
        wk_model.data['low'] = inputs['low'][index]
        wk_model.data['close'] = inputs['close'][index]
        wk_model.data['volume'] = inputs['volume'][index]
        wk_model.data['avg_volume'] = inputs['avg_volume'][index]
        wk_model.data['percent_change'] = inputs['percent_change'][index]

        return wk_model


    def make_tech_indic_model(self, inputs: dict, index: int) -> Technical_Indicators:
        # Class factory to generate each price eod's techincal anaylisis
        ta = Technical_Indicators()

        ta.data['atr_3_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=3)[index]
        ta.data['atr_10_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=10)[index]
        ta.data['atr_15_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=15)[index]
        ta.data['atr_20_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)[index]

        return ta

    
    def make_chart_idic_model(self, inputs: dict, index: int) -> Chart_Indicators:
        ca = Chart_Indicators()

        ca.data['two_crows'] = int(talib.CDL2CROWS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])
        ca.data['three_black_crows'] = int(talib.CDL3BLACKCROWS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        return ca


 # ======================================================= # 
 #            IEX API Calls                                #
 # ======================================================= #


class IEX(util.API_Request):

    def __init__(self, ticker: str):
        self.base = super()
        self.ticker = ticker
        self.api_key = 'KBE1FWN6A9NDD5JR'
        #self.data = self.try_api_call(is_daily)
        with open('./' + ticker + '-advanced-stats.json') as f:
            self.data = json.load(f)
        with open('./' + ticker + '-balance-sheet.json') as f:
            bs = json.load(f)
        bs = bs['balancesheet'][0]
        self.data = {**bs, **self.data}
        with open('./' + ticker + '-cashflows.json') as f:
            cs = json.load(f)
        cs = cs['cashflow'][0]
        self.data = {**cs, **self.data}
        with open('./' + ticker + '-income.json') as f:
            inc = json.load(f)
        inc = inc['income'][0]
        self.data = {**inc, **self.data}
        return


    def make_fund_indic_model(self) -> Fundamental_Indicators:
        fa = Fundamental_Indicators()

        fa.data['total_revenue'] = float(self.data['totalRevenue'])
        fa.data['cost_of_revenue'] = float(self.data['costOfRevenue'])
        
        return fa

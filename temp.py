#! /usr/bin/env python
from data_operations.database.helpers import DB
from data_operations.utils.api_requests import AlphaVantage, IEX
from shared.models import Price_EOD, Technical_Indicators, Chart_Indicators, Ticker, Price_Weekly

from datetime import datetime, date
import numpy as np
import talib
from copy import deepcopy


db = DB()
tick = Ticker()

tick.basic_info.data['date'] = datetime.now().date()
tick.basic_info.data['ticker'] = 'MCF'

fa = IEX('mcf')
fa_data = fa.make_fund_indic_model()
tick.fund_anaylsis = fa_data

# stop each array after x number of days we dont need the whole thing
symbol = AlphaVantage('MCF')
symbol_wk = AlphaVantage('MCF', False)
inputs = symbol.get_inputs()
wk_inputs = symbol_wk.get_inputs()
start = len(inputs['date']) - 1
end = start - 5
test =[]
for index in range(start, end, -1):
  wk_data = symbol_wk.make_price_wk_model(wk_inputs, index)
  tick.weekly.append(wk_data)

  eod_data = symbol.make_price_eod_model(inputs, index)
  tick.eod.append(eod_data)

  tech_data = symbol.make_tech_indic_model(inputs, index)
  tick.tech_anaylsis.append(tech_data)

  chart_data = symbol.make_chart_idic_model(inputs, index)
  tick.chart_anaylsis.append(chart_data)

# if whatever reason we fail, dont bother saving
db.save_ticker_model(tick)

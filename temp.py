#! /usr/bin/env python
from data_operations.database.helpers import DB
from data_operations.utils.api_requests import AlphaVantage, IEX
from shared.models import Price_EOD, Ticker

from datetime import datetime, date


db = DB()
tick = Ticker()

tick.basic_info.data['date'] = datetime.now().date()
tick.basic_info.data['ticker'] = 'MCF'

fa = IEX('mcf')
fa_data = fa.make_fund_indic_model()
# Need TD here to add values for shorites and w.e
tick.fund_anaylsis = fa_data

# stop each array after x number of days we dont need the whole thing
sp = AlphaVantage('.ixc')
sp_inputs = sp.get_inputs()
symbol = AlphaVantage('mcf')
symbol_wk = AlphaVantage('mcf', False)
inputs = symbol.get_inputs()
wk_inputs = symbol_wk.get_inputs()
inputs['s_p'] = sp_inputs['close']
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

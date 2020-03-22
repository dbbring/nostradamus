#! /usr/bin/env python
from data_operations.database.helpers import DB
from shared.models import Ticker
from datetime import datetime, date

db = DB()
tick = Ticker()

tick.basic_info.data['date'] = datetime.now().date()
tick.basic_info.data['ticker'] = 'MSFT'
db.save(tick.basic_info)
transaction_id = db.last_insert_id

tick.fund_anaylsis.data['transaction_id'] = transaction_id
tick.fund_anaylsis.data['earnings_date'] = datetime.now().date()
tick.fund_anaylsis.data['balance_sheet_date'] = datetime.now().date()
db.save(tick.fund_anaylsis)

tick.eod[0].data['date'] = datetime.now().date()
tick.eod[0].data['is_tracking_period'] = True

for index, eod_data in enumerate(tick.eod):
  eod_data.data['transaction_id'] = transaction_id
  db.save(eod_data)
  eod_id = db.last_insert_id
  tick.tech_anaylsis[index].data['eod_id'] = eod_id
  tick.chart_anaylsis[index].data['eod_id'] = eod_id
  db.save(tick.chart_anaylsis[index])
  db.save(tick.tech_anaylsis[index])

tick.weekly[0].data['wk_start_date'] = datetime.now().date()
tick.weekly[0].data['wk_end_date'] = datetime.now().date()
for week in tick.weekly:
  week.data['transaction_id'] = transaction_id
  db.save(week)

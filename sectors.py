#! /usr/bin/env python

from data_operations.utils.scrapers import Bloomberg, TDAmeritrade
from data_operations.database.helpers import DB
from shared.models import Sectors
from data_operations.utils.helpers import send_mail

from datetime import date, datetime

try:
  mySQL = DB()
  model = Sectors()
  today = datetime.now().date()

  bloomberg = Bloomberg()

  model.data['date'] = today
  model.data['s_p'] = bloomberg.sectors['all sectors']
  model.data['real_estate'] = bloomberg.sectors['real estate']
  model.data['consumer_staples'] = bloomberg.sectors['consumer staples']
  model.data['health_care'] = bloomberg.sectors['health care']
  model.data['utilities'] = bloomberg.sectors['utilities']
  model.data['materials'] = bloomberg.sectors['materials']
  model.data['industrials'] = bloomberg.sectors['industrials']
  model.data['financials'] = bloomberg.sectors['financials']
  model.data['energy'] = bloomberg.sectors['energy']
  model.data['communication_services'] = bloomberg.sectors['communication services']
  model.data['consumer_discretionary'] = bloomberg.sectors['consumer discretionary']
  model.data['information_technology'] = bloomberg.sectors['information technology']

  td_dji = TDAmeritrade('$DJI', True)
  model.data['dji'] = td_dji.get_percent_change()

  td_vix = TDAmeritrade('$VIX.X', True)
  model.data['vix'] = td_vix.get_percent_change()
  model.data['vix_close'] = td_vix.get_price()

  td_nasdaq = TDAmeritrade('$COMPX', True)
  model.data['nasdaq'] = td_nasdaq.get_percent_change()

  td_rus_1000 = TDAmeritrade('$RUI.X', True)
  model.data['russell_1000'] = td_rus_1000.get_percent_change()

  td_rus_2000 = TDAmeritrade('$RUT.X', True)
  model.data['russell_2000'] = td_rus_2000.get_percent_change()


  mySQL.save(model)

  send_mail('Sectors Script Succesfully Executed')
except Exception as ex:
  send_mail('Sectors Script Failed!! ' + str(ex))




from data_operations.utils.scrapers import Bloomberg
from data_operations.database.helpers import DB
from data_operations.utils.api_requests import AlphaVantage, Fin_Mod_Prep
from shared.models import Sectors

from datetime import date, datetime


mySQL = DB()
model = Sectors()
today = datetime.now().date()


bloomberg = Bloomberg()

model.schema['date'] = today
model.schema['s_p'] = bloomberg.sectors['all sectors']
model.schema['real_estate'] = bloomberg.sectors['real estate']
model.schema['consumer_staples'] = bloomberg.sectors['consumer staples']
model.schema['health_care'] = bloomberg.sectors['health care']
model.schema['utilities'] = bloomberg.sectors['utilities']
model.schema['materials'] = bloomberg.sectors['materials']
model.schema['industrials'] = bloomberg.sectors['industrials']
model.schema['financials'] = bloomberg.sectors['financials']
model.schema['energy'] = bloomberg.sectors['energy']
model.schema['communication_services'] = bloomberg.sectors['communication services']
model.schema['consumer_discretionary'] = bloomberg.sectors['consumer discretionary']
model.schema['information_technology'] = bloomberg.sectors['information technology']

fin_mod_prep = Fin_Mod_Prep()
indicies = fin_mod_prep.get_indices()

for ticker in indicies:
  if ticker['indexName'] == 'Dow Jones':
    model.schema['dji'] = model.to_percent_with_diff(ticker['price'], ticker['changes'])
  elif ticker['indexName'] == 'Nasdaq':
    model.schema['nasdaq'] = model.to_percent_with_diff(ticker['price'], ticker['changes'])
  elif ticker['indexName'] == 'Russell 1000 Index':
    model.schema['russell_1000'] =model.to_percent_with_diff(ticker['price'], ticker['changes'])
  elif ticker['indexName'] == 'Russell 2000 Index':
    model.schema['russell_2000'] = model.to_percent_with_diff(ticker['price'], ticker['changes'])

av = AlphaVantage('VIX')

vix_today = av.data[today.strftime('%Y-%m-%d')]
model.schema['vix'] = model.to_percent(float(vix_today['4. close']), float(vix_today['1. open']))
model.schema['vix_close'] = float(vix_today['4. close'])


mySQL.save(model)
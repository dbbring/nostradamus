from data_operations.utils.scrapers import *
from data_operations.database.helpers import *
from shared.models import Sectors

from datetime import date, datetime

sector_performance = Bloomberg()
mySQL = DB()
model = Sectors()

model.schema['date'] = datetime.now().date()
model.schema['s_p'] = sector_performance.sectors['all sectors']
model.schema['real_estate'] = sector_performance.sectors['real estate']
model.schema['consumer_staples'] = sector_performance.sectors['consumer staples']
model.schema['health_care'] = sector_performance.sectors['health care']
model.schema['utilities'] = sector_performance.sectors['utilities']
model.schema['materials'] = sector_performance.sectors['materials']
model.schema['industrials'] = sector_performance.sectors['industrials']
model.schema['financials'] = sector_performance.sectors['financials']
model.schema['energy'] = sector_performance.sectors['energy']
model.schema['communication_services'] = sector_performance.sectors['communication services']
model.schema['consumer_discretionary'] = sector_performance.sectors['consumer discretionary']
model.schema['information_technology'] = sector_performance.sectors['information technology']

mySQL.save(model)
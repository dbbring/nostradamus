from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Sectors as Sectors_Model
from datetime import datetime, timedelta
from data_operations.utils.api_requests import AlphaVantage
from os import path
from json import loads as json_loads

class Sectors(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    self.five_day_performance = {}
    self.one_month_performance = {}
    self.three_month_performance = {}
    self.ytd_performance = {}
    self.one_year_performance = {}
    self.three_year_performance = {}
    self.load_monthly_sectors()
    return
    
  def get(self, date: str, sector_name=None) -> dict:
    if sector_name == None:
      results = self.query_db(self.config['sectors']['database_name'], f"SELECT * FROM Sectors WHERE date = '{date}';")
      return self.make_sector_model(results)
    else:
      clean_sector_name = Sectors_Model.get_sector(self, sector_name)
      results = self.query_db(self.config['sectors']['database_name'], f"SELECT sector_id, date, s_p, dji, nasdaq, russell_1000, russell_2000, vix, vix_close, {clean_sector_name} FROM Sectors WHERE date = '{date}';")
      return self.make_custom_sector_model(results, clean_sector_name)

  def make_sector_model(self, sql_results: list):
    all_results = []

    for item in sql_results:
      model = Sectors_Model()
      model.data['sector_id'] = item[0]
      model.data['date'] = item[1].strftime('%Y-%m-%d') if item[1] else item[1]
      model.data['s_p'] = item[2]
      model.data['dji'] = item[3]
      model.data['nasdaq'] = item[4]
      model.data['russell_1000'] = item[5]
      model.data['russell_2000'] = item[6]
      model.data['vix'] = item[7]
      model.data['vix_close'] = item[8]
      model.data['real_estate'] = item[9]
      model.data['consumer_staples'] = item[10]
      model.data['health_care'] = item[11]
      model.data['utilities'] = item[12]
      model.data['materials'] = item[13]
      model.data['industrials'] = item[14]
      model.data['financials'] = item[15]
      model.data['energy'] = item[16]
      model.data['communication_services'] = item[17]
      model.data['consumer_discretionary'] = item[18]
      model.data['information_technology'] = item[19]

      all_results.append(model.data)

    return all_results

  def make_custom_sector_model(self, sql_results: list, column: str):
    all_results = []

    for item in sql_results:
      model = {}
      model['sector_id'] = item[0]
      model['date'] = item[1].strftime('%Y-%m-%d') if item[1] else item[1]
      model['s_p'] = item[2]
      model['dji'] = item[3]
      model['nasdaq'] = item[4]
      model['russell_1000'] = item[5]
      model['russell_2000'] = item[6]
      model['vix'] = item[7]
      model['vix_close'] = item[8]
      model[column] = item[9]

      all_results.append(model)

    return all_results

  def load_monthly_sectors(self):
    timestamp = path.getmtime('sector_performance.json')
    wk_ago = datetime.today() - timedelta(days=7)
    if timestamp < wk_ago:
      # https://www.alphavantage.co/query?function=SECTOR&apikey=KBE1FWN6A9NDD5JR
      av = 'test'
      # json dumps into sector_performance.json
    else:
      all_sectors = json_loads('sector_performance.json')
    return
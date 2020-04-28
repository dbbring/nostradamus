from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Transaction
from datetime import datetime

class Index(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    return
    
  def get(self, date=None) -> dict:
    if date == None:
      return self.get_all()
    else:
      return self.get_all_by_date(date)
    return {}


  def get_all(self):
    all_results = []

    for data_item in self.config['nostradamus']:
      result = self.query(data_item['api_endpoint'], "SELECT * FROM Transaction;")
      all_results = all_results + self.make_transaction_model(result)

    return all_results

  def get_all_by_date(self,date):
    all_results = []

    for data_item in self.config['nostradamus']:
      result = self.query(data_item['api_endpoint'], f"SELECT * FROM Transaction WHERE date = '{date}';")
      all_results = all_results + self.make_transaction_model(result)

    return all_results

  def get_by_id(self, api_endpoint:str, transaction_id: int):
    result = self.query(api_endpoint, f"SELECT * FROM Transaction WHERE transaction_id = '{transaction_id}';")
    return self.make_transaction_model(result)


  def get_db_specific(self, api_endpoint: str):
    result = self.query(api_endpoint, "SELECT * FROM Transaction;")
    return self.make_transaction_model(result)

  def get_db_specific_by_date(self, api_endpoint: str, date: str):
    result = self.query(api_endpoint, f"SELECT * FROM Transaction WHERE date = '{date}';")
    return self.make_transaction_model(result)

  # list of dicts (data objects)
  def make_transaction_model(self, sql_results: list) -> list:
    all_results = []
    for trans_item in sql_results:
      model = Transaction()
      model.data['transaction_id'] = trans_item[0]
      model.data['date'] = trans_item[1].strftime('%Y-%m-%d') if trans_item[1] else None
      model.data['ticker'] = trans_item[2]
      model.data['percent_change'] = trans_item[3]
      all_results.append(model.data)

    return all_results

class IndexSpecific(Index):

  def __init__(self):
    super().__init__()
    return

  def get(self, api_endpoint, date=None):
    if date == None:
      return self.get_db_specific(api_endpoint)
    else:
      return self.get_db_specific_by_date(api_endpoint, date)
    return {}
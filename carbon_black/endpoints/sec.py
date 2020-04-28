from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import SEC as SEC_Model, SEC_Company_Info, SEC_Employee_Stock, SEC_Merger, SEC_Secondary_Offering
from datetime import datetime
from json import loads as json_loads

class SEC(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    self.api_endpoint = None
    return
    
  def get(self, api_endpoint:str, transaction_id:int) -> dict:
    self.api_endpoint = api_endpoint
    results = self.query(api_endpoint, f"SELECT * FROM SEC WHERE transaction_id = {transaction_id};")
    return self.make_sec_model(results)

  def make_sec_model(self, sql_results: list):
    all_results = []

    for item in sql_results:
      model = SEC_Model()
      model.data['sec_id'] = item[0]
      model.data['transaction_id'] = item[1]
      model.data['date_of_ipo'] = item[2].strftime('%Y-%m-%d')
      model.data['late_filings'] = item[3]
      model.data['ct_orders'] = item[4]
      model.data['is_adr'] = bool(item[5])

      model.data['company_info'] = self.make_company_info(item[0])
      model.data['secondary_offerings'] = self.make_secondary_offering(item[0])
      model.data['mergers'] = self.make_mergers(item[0])
      model.data['stock_program'] = self.make_stock_program(item[0])

      all_results.append(model.data)

    return all_results


  def make_secondary_offering(self, sec_id: int) -> list:
    all_results = []
    results = self.query(self.api_endpoint, f"SELECT * FROM SEC_Secondary_Offering WHERE sec_id = {sec_id};")

    for item in results:
      model = SEC_Secondary_Offering()
      model.data['sec_secondary_offering_id'] = item[0]
      model.data['sec_id'] = item[1]
      model.data['date'] = item[2].strftime('%Y-%m-%d') if item[2] else None
      model.data['additional_shares_issued'] = item[3]
      model.data['is_asr'] = bool(item[4])
      model.data['link'] = item[5]

      all_results.append(model.data)

    return all_results

  
  def make_company_info(self, sec_id: int) -> list:
    all_results = []
    results = self.query(self.api_endpoint, f"SELECT * FROM SEC_Company_Info WHERE sec_id = {sec_id};")

    for item in results:
      model = SEC_Company_Info()
      model.data['sec_company_info_id'] = item[0]
      model.data['sec_id'] = item[1]
      model.data['date'] = item[2].strftime('%Y-%m-%d') if item[2] else None
      model.data['link'] = item[3]
      model.data['item_list'] = json_loads(item[4])

      all_results.append(model.data)

    return all_results

  def make_mergers(self, sec_id: int) -> list:
    all_results = []
    results = self.query(self.api_endpoint, f"SELECT * FROM SEC_Merger WHERE sec_id = {sec_id};")

    for item in results:
      model = SEC_Merger()
      model.data['sec_merger_id'] = item[0]
      model.data['sec_id'] = item[1]
      model.data['date'] = item[2].strftime('%Y-%m-%d') if item[2] else None
      model.data['merging_with_company'] = item[3]
      model.data['merging_with_cik'] = item[4]

      all_results.append(model.data)

    return all_results

  def make_stock_program(self, sec_id: int) -> list:
    all_results = []
    results = self.query(self.api_endpoint, f"SELECT * FROM SEC_Employee_Stock WHERE sec_id = {sec_id};")

    for item in results:
      model = SEC_Secondary_Offering()
      model.data['sec_employee_stock_id'] = item[0]
      model.data['sec_id'] = item[1]
      model.data['date'] = item[2].strftime('%Y-%m-%d') if item[2] else None
      model.data['additional_shares_issued'] = item[3]
      model.data['link'] = item[4]

      all_results.append(model.data)

    return all_results
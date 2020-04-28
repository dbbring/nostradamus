from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Peer_Performance
from datetime import datetime

class Peers(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    return
    
  def get(self, api_endpoint:str, transaction_id:int) -> dict:
    results = self.query(api_endpoint, f"SELECT * FROM Peer_Performance WHERE transaction_id = {transaction_id};")
    return self.make_peers_model(results)

  def make_peers_model(self, sql_results: list):
    all_results = []

    for item in sql_results:
      model = Peer_Performance()
      model.data['eod_id'] = item[0]
      model.data['transaction_id'] = item[1]
      model.data['date'] = item[2].strftime('%Y-%m-%d') if item[2] else None
      model.data['open'] = item[3]
      model.data['high'] = item[4]
      model.data['low'] = item[5]
      model.data['close'] = item[6]
      model.data['volume'] = item[7]
      model.data['percent_change'] = item[8]
      model.data['ticker'] = item[9]

      all_results.append(model.data)

    return all_results
from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Chart_Indicators
import datetime

class Charting(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    return
    
  def get(self, api_endpoint:str, transaction_id:int) -> dict:
    result = super().query(api_endpoint, f"SELECT * FROM Transaction WHERE transaction_id = {transaction_id};")
    return {
        'id': result[0][0],
        'date': result[0][1].strftime("%m/%d/%Y"),
        'ticker': result[0][2],
        'percent change': result[0][3]
      }

  def make_chart_model(self):
    model = Chart_Indicators()

    return model
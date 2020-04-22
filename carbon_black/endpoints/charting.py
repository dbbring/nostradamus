from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Chart_Indicators

class Charting(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    return
    
  def get(self, database_name:str, transaction_id:int) -> dict:
    model = self.make_chart_model()
    return model.data

  def make_chart_model(self):
    model = Chart_Indicators()

    return model
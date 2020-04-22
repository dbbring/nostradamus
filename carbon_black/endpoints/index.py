from carbon_black.endpoints.base_endpoint import Endpoint

class Index(Endpoint):

  def __init__(self) -> None:
    self.base = super().__init__()
    return
    
  def get(self, database_name: str) -> dict:
    self.base.get_db(database_name)
    return {'hello': 'world'}
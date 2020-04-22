from carbon_black.endpoints.base_endpoint import Endpoint

class DNA(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    return
    
  def get(self):
    return {'hello': 'world'}
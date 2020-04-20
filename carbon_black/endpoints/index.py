from carbon_black.endpoints.base_endpoint import Endpoint

class Index(Endpoint):

  def __init__(self, db_name: str) -> None:
    super().__init__()
    self.response = {}
    return 
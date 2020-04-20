from carbon_black.endpoints.base_endpoint import Endpoint

class Sectors(Endpoint):

  def __init__(self, db_name: str) -> None:
    self.response = {}
    return 
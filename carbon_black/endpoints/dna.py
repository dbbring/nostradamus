from carbon_black.endpoints.base_endpoint import Endpoint

class DNA(Endpoint):

  def __init__(self, db_name: str, transaction_id: int) -> None:
    self.response = {}
    return 
from carbon_black.endpoints.base_endpoint import Endpoint

class Peer_Performance(Endpoint):

  def __init__(self, db_name: str, transaction_id: int) -> None:
    self.response = {}
    return 
from carbon_black.endpoints.base_endpoint import Endpoint
import json
from os import path


class Nostradamus_Settings(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        settings_exist = path.exists("../data_operations/config.json")
        if not settings_exist:
            {
                'Error': 'Cant Find Setings File.'
            }
        else:
            with open('../data_operations/config.json') as f:
                self.settings = json.load(f)
        return

    def get(self) -> dict:
        try:
            return self.settings
        except Exception as err:
            return {
                'error': str(repr(err))
            }

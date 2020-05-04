from carbon_black.endpoints.base_endpoint import Endpoint
import json
from os import path
from datetime import datetime


class Settings(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        settings_exist = path.exists("settings.json")
        if not settings_exist:
            init_settings = {
                'primary_color': '#e0e0e0',
                'secondar_color': '#000'
            }

            for index, data_item in enumerate(self.config['nostradamus']):
                init_settings[data_item['api_endpoint']] = {
                    'primary_color': '#228B22' if index % 2 == 0 else '#ff0000'
                }

            self.settings = init_settings
            with open('settings.json', 'w') as f:
                json.dump(init_settings, f)
        else:
            with open('settings.json') as f:
                self.settings = json.load(f)
        return

    def get(self) -> dict:
        try:
            return self.settings
        except Exception as err:
            return {
                'error': str(repr(err))
            }

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
      }

      for data_item in self.config['nostradamus']:
        init_settings[data_item['api_endpoint']] = {
          'primary_color': '#000'
        }
        self.settings = init_settings
    else:
      with open("settings.json","a+") as f:
        self.settings = json.loads(f.read())
    return
    
  def get(self) -> dict:
    return self.settings

#! /usr/bin/env python
# ======================= Gen Imports ========================
import sys
import json
from flask import Flask
from flask_restful import Api
import os

# Stupid games so we can run our api in a nested folder. Some reason we iterate though twice and changing directories throws shit off. but we have to change directories otherwise Flask cant find us.
if 'carbon_black' not in os.getcwd():
  with open('./data_operations/config.json') as f:
              config = json.load(f)
else:
  with open('../data_operations/config.json') as f:
              config = json.load(f)

sys.path.insert(1, config['project_root'])
os.chdir(config['project_root'] + 'carbon_black')

# ====================== Custom Imports ======================

from carbon_black.endpoints import *




app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/<string:database_name>')

api.add_resource(Charting, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(DNA, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(EOD, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(Fundamental, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(News, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(Peer_Performance, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(SEC, '/chart/<string:database_name>/<int:transaction_id>')
api.add_resource(Sectors, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(Technical, '/chart/<string:database_name>/<int:transaction_id>')

api.add_resource(Weekly, '/chart/<string:database_name>/<int:transaction_id>')




app.run(debug=True)
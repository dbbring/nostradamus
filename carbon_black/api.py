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

api.add_resource(Index, '/', '/<string:date>')

api.add_resource(IndexSpecific, '/api/<string:api_endpoint>', '/api/<string:api_endpoint>/<string:date>')

api.add_resource(EOD, '/api/<string:api_endpoint>/price-eod/<int:transaction_id>/<string:include_anaylsis>')

api.add_resource(Fundamental, '/api/<string:api_endpoint>/fundamental/<int:transaction_id>')

api.add_resource(News, '/api/<string:api_endpoint>/news/<int:transaction_id>')

api.add_resource(Peers, '/api/<string:api_endpoint>/peers/<int:transaction_id>')

api.add_resource(SEC, '/api/<string:api_endpoint>/sec/<int:transaction_id>')

api.add_resource(Weekly, '/api/<string:api_endpoint>/price-weekly/<int:transaction_id>')

api.add_resource(Sectors, '/api/sectors/<string:date>')

# ============= Non Table Related (custom rolled) ===================

api.add_resource(Ticker, '/api/<string:api_endpoint>/ticker/<int:transaction_id>')

api.add_resource(DNA, '/api/<string:api_endpoint>/dna/<int:transaction_id>')

api.add_resource(Settings, '/api/settings')


app.run(debug=True)
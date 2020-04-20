#! /usr/bin/env python
# ======================= Gen Imports ========================
import sys
import json
from flask import Flask
from flask_restful import Api

# ==== Add our path to the python path so we can import our modules ====
with open('./data_operations/config.json') as f:
            config = json.load(f)

sys.path.insert(1, config['project_root'])

# ====================== Custom Imports ======================

from carbon_black.endpoints import *

app = Flask(__name__)
api = Api(app)

for data_item in config['nostradamus']:
  base_url = '/' + data_item['api_endpoint']

  api.add_resource(Index(data_item['database_name']), base_url)

  @app.route(base_url)
  def index():
    _index = Index(data_item['database_name'])
    response = _index.response
    return response

  @app.route(base_url + '/dna/')
  def dna(id):
    _dna = DNA(data_item['database_name'], id)
    response = _dna.response
    return response

  @app.route(base_url + '/techincal/')
  def techincal(id):
    _tech = Technical(data_item['database_name'], id)
    response = _tech.response
    return response

  @app.route(base_url + '/charting/')
  def charting(id):
    _chart = Charting(data_item['database_name'], id)
    response = _chart.response
    return response

  @app.route(base_url + '/fundamental/')
  def fundamental(id):
    _fund = Fundamental(data_item['database_name'], id)
    response = _fund.response
    return response

  @app.route(base_url + '/sec/')
  def sec(id):
    _sec = SEC(data_item['database_name'], id)
    response = _sec.response
    return response

  @app.route(base_url + '/eod/')
  def eod(id):
    _eod = EOD(data_item['database_name'], id)
    response = _eod.response
    return response

  @app.route(base_url + '/weekly/')
  def weekly(id):
    _wk = Weekly(data_item['database_name'], id)
    response = _wk.response
    return response

  @app.route(base_url + '/peer-performance/')
  def peer_performance(id):
    _pp = Peer_Performance(data_item['database_name'], id)
    response = _pp.response
    return response

  @app.route(base_url + '/news/')
  def news(id):
    _news = News(data_item['database_name'], id)
    response = _news.response
    return response

# Not part of the Nostradamus DB's
@app.route('/sectors/')
def sectors():
  _sectors = Sectors(config['sectors']['database_name'])
  response = _sectors.response
  return response


app.run(debug=True)
#! /usr/bin/env python
# ======================= Gen Imports ========================
import sys
import json
from flask import Flask

# ==== Add our path to the python path so we can import our modules ====
with open('./data_operations/config.json') as f:
            config = json.load(f)

sys.path.insert(1, config['project_root'])

# ====================== Custom Imports ======================

from carbon_black.endpoints import *

app = Flask(__name__)

@app.route('/')
def index():
  indx = Index()
  response = indx.response
  return response

@app.route('/dna')
def dna():
  response = DNA()
  return response

@app.route('/techincal/')
def techincal(id):
  ta = Technical(id)
  response = ta.response
  return {}

@app.route('/charting')
def charting():
  return {}

@app.route('/fundamental')
def fundamental():
  return {}

@app.route('/sec')
def sec():
  return {}

@app.route('/eod')
def eod():
  return {}

@app.route('/weekly')
def weekly():
  return {}

@app.route('/peer-performance')
def peer_performance():
  return {}

@app.route('/news')
def news():
  return {}
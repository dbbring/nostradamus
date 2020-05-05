from flask_restful import Resource
from json import load as json_load
import os

from data_operations.database.helpers import DB


class Endpoint(Resource):

    def __init__(self):
        if 'carbon_black' not in os.getcwd():
            with open('./data_operations/config.json') as f:
                self.config = json_load(f)
        else:
            with open('../data_operations/config.json') as f:
                self.config = json_load(f)
        return

    def query_db(self, db_name: str, query: str):
        results = []
        db = DB(db_name, False)
        try:
            results = db.select(query)
            return results
        except Exception as err:
            print(err)
            return []

    # returns a list of tuples from sql execucation

    def query(self, api_endpoint: str, query: str) -> list:
        db = None
        results = []

        for data_item in self.config['nostradamus']:
            if data_item['api_endpoint'] == api_endpoint:
                db = DB(data_item['database_name'])

        if db == None:
            return

        results = db.select(query)
        del db
        return results

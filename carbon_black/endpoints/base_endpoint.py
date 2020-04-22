from flask_restful import Resource
from data_operations.database.helpers import DB

class Endpoint(Resource):

  def __init__(self):
    self.db = None
    return

  def get_db(self, db_name: str):
    self.db = DB(db_name)
    return db

  def select_all(self, db_name: str, table: str):
    if self.db == None:
      return None

    
    return


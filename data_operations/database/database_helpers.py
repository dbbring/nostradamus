class DB(object):
    
    def __init__(self):
        return

    @property
    def db(self): 
        return 'db'   
    @db.setter
    def db(self, value):
        self.db = value
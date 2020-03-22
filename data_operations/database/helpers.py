from data_operations.database.sql import DB_SCHEMA
import mysql.connector
from mysql.connector import errorcode

class DB(DB_SCHEMA):
    
    def __init__(self):
        self.base = super()
        self.insert_sql = self.base.insert_statements()
        self.update_sql = self.base.update_statements()
        self.last_insert_id = -1
        try:
            self.cnx = mysql.connector.connect(user='toor', database='nostradamus')
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        self.load_tables()
        return

    
    def __del__(self):
        self.cnx.close()
        return
    

    def load_tables(self):
        base_tables = self.base.tables()
        for table_name in base_tables:
            table_description = base_tables[table_name]
            try:
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                print(err.msg)
        return


    def save(self, model) -> None:
        data = list(model.data.values())
        if not data[0]:  # if our id is null, then exclude it
            del data[0]
        self.cursor.execute(self.insert_sql[type(model).__name__], data)
        self.last_insert_id = self.cursor.lastrowid
        self.cnx.commit()
        return

    def update(self, model) -> None:
        # use update statements here.
        # figure out which key changed i guess
        # update [ dict key ] values [ dict value ]
        return


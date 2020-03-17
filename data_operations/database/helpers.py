from data_operations.database.sql import db_schema
import mysql.connector
from mysql.connector import errorcode

class DB(db_schema):
    
    def __init__(self):
        self.base = super()
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
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
        return


    def save(self, model) -> None:
        table_name = type(model).__name__
        data = list(model.data.values())
        
        if not data[0]:  # if our id is null, then exclude it
            del data[0]
            self.cursor.execute(model.insert_sql, data)
            self.cnx.commit()
            return

        # do updates here because we need the id
        return


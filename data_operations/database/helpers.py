from data_operations.database.sql import DB_SCHEMA
from shared.models import Ticker

from datetime import datetime, timedelta
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
        # self.cursor.close()
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


    def save_ticker_model(self, ticker_model: Ticker) -> None:
        self.save(ticker_model.basic_info)
        trans_id = self.last_insert_id

        
        ticker_model.fund_anaylsis.data['transaction_id'] = trans_id
        self.save(ticker_model.fund_anaylsis)

        for item in ticker_model.weekly:
            item.data['transaction_id'] = trans_id
            self.save(item)

        for index, item in enumerate(ticker_model.eod):
            item.data['transaction_id'] = trans_id
            self.save(item)
            eod_id = self.last_insert_id

            ta = ticker_model.tech_anaylsis[index]
            ta.data['eod_id'] = eod_id
            self.save(ta)

            ca = ticker_model.chart_anaylsis[index]
            ca.data['eod_id'] = eod_id
            self.save(ca)

        return


    def update_ticker_model(self, ticker_model: Ticker) -> None:
        models = vars(ticker_model).keys()
        for model in models:
            item = getattr(ticker_model, model)
            if type(item) is not list:
                self.update(model)
            else:
                for nest_model in model:
                    self.update(nest_model)

        return


    def update(self, model) -> None:
        data = list(model.data.values())
        if not data[0]:  # if our id is null, then exclude it
            del data[0]
        self.cursor.execute(self.update_sql[type(model).__name__], data)
        self.cnx.commit()
        return

 # @returns a list of tuples with id and ticker
    def select_tracking_tickers(self) -> list:
        tickers = []
        # get last 5 days, which is actually 7 days from any point in the week
        lookback_date = datetime.today() - timedelta(days=7)
        lookback_date = lookback_date.strftime("%Y-%m-%d")
        sql = "SELECT transaction_id, ticker FROM Transaction WHERE date = '" + lookback_date + "';"
        self.cursor.execute(sql)

        for ticker in self.cursor:
            tickers.append(ticker)

        return tickers


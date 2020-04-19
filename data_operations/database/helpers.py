#! /usr/bin/env python
# ==================== Gen Imports ===========================
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import errorcode
from json import dumps



# =================== Custom Imports ========================
from data_operations.database.sql import DB_SCHEMA
from shared.models import Ticker


# ==============================================================
#                   Database Connection Class
# ==============================================================

class DB(DB_SCHEMA):
    
    # @params (database_name) - Name of DB instance to be using
    # @descrip - Connects to MySQL Instance and checks for database nostradamus, and loads up table in not present
    # @returns None
    def __init__(self, database_name:str, is_nostradamus_db=True):
        self.base = super()
        self.is_nostradamus_db = is_nostradamus_db
        self.insert_sql = self.base.insert_statements()
        self.update_sql = self.base.update_statements()
        self.last_insert_id = -1
        try:
            self.cnx = mysql.connector.connect(user='toor', database=database_name)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        base_tables = self.base.nostradamus_tables() if is_nostradamus_db else self.base.sectors_tables()
        self.load_tables(base_tables)
        return


    # @params (None)
    # @descrip - Destructor, when we are done close up connections
    # @returns None
    def __del__(self):
        self.cnx.close()
        return
    

    # @params (None)
    # @descrip - Loads table from SQL file
    # @returns None
    def load_tables(self, tables: dict) -> None:
        for table_name in tables:
            table_description = tables[table_name]
            try:
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                print(err.msg)
        return


    # @params (model) a instance of a model
    # @descrip - Save a singluar instance of model and set class level field to last inserted in
    # @returns None
    def save(self, model) -> None:
        data = list(model.data.values())
        if not data[0]:  # if our id is null, then exclude it
            del data[0]
        self.cursor.execute(self.insert_sql[type(model).__name__], data)
        self.last_insert_id = self.cursor.lastrowid
        self.cnx.commit()
        return


    # @params (ticker_model) a instance of the class model of ticker
    # @descrip - Saves a ticker model which consists of models and array of models
    # @returns None
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
        
        for news_model in ticker_model.news:
            news_model.data['transaction_id'] = trans_id
            self.save(news_model)
        
        for peer in ticker_model.peers:
            peer.data['transaction_id'] = trans_id
            self.save(peer)

        # store off sec info copy list dont reference it
        company_info = list(ticker_model.sec.data['company_info'])
        secon_offer = list(ticker_model.sec.data['secondary_offerings'])
        mergers = list(ticker_model.sec.data['mergers'])
        stock_program = list(ticker_model.sec.data['stock_program'])
        # remove arrays so we can save and our model matches up with the table
        del ticker_model.sec.data['company_info']
        del ticker_model.sec.data['secondary_offerings']
        del ticker_model.sec.data['mergers']
        del ticker_model.sec.data['stock_program']

        ticker_model.sec.data['transaction_id'] = trans_id
        self.save(ticker_model.sec)
        sec_id = self.last_insert_id
        
        # now save off seperate tables
        for merger in mergers:
            merger.data['sec_id'] = sec_id
            self.save(merger)

        for offering in secon_offer:
            offering.data['sec_id'] = sec_id
            self.save(offering)

        for info in company_info:
            info.data['sec_id'] = sec_id
            # MySQL doesnt coerce dicts to json so we have manually move it over
            info.data['item_list'] = dumps(info.data['item_list'])
            self.save(info)

        for incentive in stock_program:
            incentive.data['sec_id'] = sec_id
            self.save(incentive)
        
        return


    # @params (Ticker_Model) a instance of the class ticker
    # @descrip - Not using yet! IDK if it works..you have been warned...
    # @returns None
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


    # @params (model) a instance of a model
    # @descrip - Not using yet! IDK if it works..you have been warned...
    # @returns None
    def update(self, model) -> None:
        data = list(model.data.values())
        if not data[0]:  # if our id is null, then exclude it
            del data[0]
        self.cursor.execute(self.update_sql[type(model).__name__], data)
        self.cnx.commit()
        return


    # @params (None)
    # @descrip - Query DB and return all tickers that need the price performance tracked for the last x days
    # @returns list - a list of tuples with id and ticker
    def select_tracking_tickers(self) -> list:
        if self.is_nostradamus_db:
            tickers = []
            # get last 5 days, which is actually 7 days from any point in the week
            # ^ Holidays might screw us? Meh...
            lookback_date = datetime.today() - timedelta(days=7)
            lookback_date = lookback_date.strftime("%Y-%m-%d")
            sql = "SELECT transaction_id, ticker FROM Transaction WHERE date = '" + lookback_date + "';"
            self.cursor.execute(sql)

            for ticker in self.cursor:
                tickers.append(ticker)

            return tickers
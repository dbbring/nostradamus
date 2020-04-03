#! /usr/bin/env python
# ====================== Gen Imports =========================
from bs4 import BeautifulSoup
import unicodedata
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests

# ===================== Custom Imports =======================
import data_operations.utils.helpers as util


# ============================================================ # 
#                   Abstract Class                             #
# ============================================================ #

class Scaper(object):
    
    def __init__(self):
        return


    # @params (path) - url or filepath, (use_firefox) - use headless firefox to get html
    # @descrip - Parses the HTML doc, or the webpage
    # @returns BS4 obj - a soup obj ready for other text extraction
    def get_data(self, path: str, use_firefox=False) -> BeautifulSoup:
        try:
            html = open(path, encoding='utf-8')
        except:
            if (use_firefox):
                options = Options()
                options.headless = True
                browser = webdriver.Firefox(executable_path='/home/derek/Desktop/nostradamus/.venv/lib/geckodriver',options=options)
                browser.get(path)
                html = browser.page_source
                browser.close()
            else:
                res = requests.get(url=path)
                html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup


    # @params (row) - html TR, (column) - which column holds the data, (get_text) - return the html element, or the actual text
    # @descrip - for HTML tables, return the cell of the table
    # @returns bool - true if the string is a valid float, false if not
    def get_table_cell(self, row, column, get_text:bool) -> str:
        table_cells = row.find_all('td')
        if get_text:
            return table_cells[column].get_text()
        return table_cells[column]


 # =========================================================== # 
 #                 Bloomberg scraper                            #
 # ============================================================ #

class Bloomberg(Scaper):

    # @params (None) 
    # @descrip - scrapes bloomberg sectors and populates the sectors dict for future use.
    # @returns None
    def __init__(self):
        self.sectors = {}
        soup = super().get_data('https://www.bloomberg.com/markets/sectors', True)
        table_rows = soup.find_all('div', class_='sector-data-table__sector-row')
        for row in table_rows:
            sector_name = row.contents[1].get_text().strip().lower()
            sector_performance = row.contents[3].get_text().strip()
            sector_performance = sector_performance[:(len(sector_performance) - 1)]
            if (util.isValidFloat(sector_performance)):
                self.sectors[sector_name] = float(sector_performance)
        return


 # =========================================================== # 
 #                 Finviz scraper                               #
 # ============================================================ #

class FinViz(Scaper):
    
    # @params (path) - URL or file path of the resource 
    # @descrip - scrapes Finviz and populates a BS4 Obj
    # @returns None
    def __init__(self, path: str):
        self.base = super()
        self.soup = self.base.get_data(path)
        return
    

    # @params (Upper_threshold) - Only find tickers that have at this value and below,  (Lower_threshold) - Only find tickers that have at this value and above 
    # @descrip - scrapes single webpage for tickers
    # @returns list - list of tickers that met the parameter criteria
    def get_tickers(self, upper_threshold: float, lower_threhold: float) -> list:
        tickers =[]
        self.table = self.soup.find('table', attrs={'bgcolor': '#d3d3d3', 'border': '0', 'cellpadding': '3', 'cellspacing': '1', 'width': '100%'})
        table_rows = self.table.find_all('tr')
        for row in table_rows:
            change = self.base.get_table_cell(row, 9, True)
            change = change[:-1]
            if (util.isValidFloat(change)):
                if (lower_threhold <= float(change) <= upper_threshold):
                    tickers.append(self.base.get_table_cell(row, 1, True))
        return tickers


    # @params (None) 
    # @descrip - find last row id of the web page. Finviz will give you the same last id for subsquent pages.
    # @returns int - value of last row item on finviz
    def get_last_finviz_row_id(self) -> int:
        table_rows = self.table.find_all('tr')
        for row in table_rows:
            last_id = self.base.get_table_cell(row, 0, True)
            if (util.isValidInt(last_id)):
                last_id = int(last_id)
        return last_id


    # @params (None) 
    # @descrip - finds the date of the last news article and checks to see if it was in the date ranges specified in utils.
    # @returns bool - true if we find a news article, false if not
    def has_finviz_news(self) -> bool:
        row_count = 0
        table = self.soup.find('table', id='news-table')
        table_rows = table.find_all('tr')

        for row in table_rows:
            if (row_count >= 15):
                break

            latest_news_date = self.base.get_table_cell(row, 0, True)
            latest_news_date = unicodedata.normalize('NFKD', latest_news_date).strip()  # Drop Ending Bytes
            latest_news_date = util.string_to_date(latest_news_date)
            row_count += 1

            if (latest_news_date != None):
                for date in util.get_date_ranges():
                    if (latest_news_date == date):
                        return True
        return False


 # =========================================================== # 
 #                 TD Ameritrade scraper                        #
 # ============================================================ #

class TDAmeritrade(Scaper):

    # @params (ticker) - symbol to find, (index) = is the ticker a indice? 
    # @descrip - sets up a BS4 Obj webpage
    # @returns None
    def __init__(self, ticker: str, index=False):
        self.base = super()
        if (index):
            self.soup = self.base.get_data('https://research.tdameritrade.com/grid/public/research/stocks/charts?symbol=' + ticker)
        else:
            # self.soup = self.base.get_data('https://research.tdameritrade.com/grid/public/research/stocks/summary?fromPage=overview&display=&fromSearch=true&symbol=' + ticker) 
            self.soup = self.base.get_data('../nostradamus_files/td-' + ticker + '.html')
        return


    # @params (None)
    # @descrip - finds the date of the last news article and checks to see if it was in the date ranges specified in utils.
    # @returns bool - Yes if TDAmeritrade has news, no if not
    def has_td_news(self) -> bool:
        table = self.soup.find('table', class_='latestNews')
        table_section = table.find_all('tbody')
        latest_news_date = table_section[0].find('tr').get_text()
        latest_news_date = util.string_to_date(latest_news_date)
        if (latest_news_date != None):
            for date in util.get_date_ranges():
                if (latest_news_date == date):
                    return True
        return False


    # @params (None)
    # @descrip - finds sector on TD page with the format( TopLevel : SubLevel | Description ) and extracts the text
    # @returns dict - dict of strings of the top level and sub level sectors strings literals.
    def get_sector(self) -> dict:
        sectors = {}
        sector = self.soup.find('div', class_='company-detail-information')
        sector = sector.get_text().split(':') 
        tl_sector = unicodedata.normalize('NFKD', sector[0]).strip()
        if len(sector) <= 1:
            sectors['top-level'] = tl_sector.lower()
            sectors['second-level'] = None
            return

        sl_sector = sector[1].split('|')
        sl_sector = unicodedata.normalize('NFKD', sl_sector[0]).strip()
        sectors['top-level'] = tl_sector.lower()
        sectors['second-level'] = sl_sector.lower()
        return sectors


    # @params (None)
    # @descrip - finds the institutional ownership value and parses it
    # @returns float -  TDameri's value for tute ownership
    def get_tute_ownership(self) -> float:
        tutes = self.soup.find('a', text="% Held by Institutions")
        tutes = tutes.parent.parent.find_next_sibling('dd')
        tutes = tutes.get_text()
        if util.isValidFloat(tutes):
            return float(tutes)
        return 0


    # @params (None)
    # @descrip - finds the short intrest value and parses it
    # @returns float -  TDameri's value for short intrest
    def get_short_intrest(self) -> float:
        shorties = self.soup.find('a', text="Short Interest")
        shorties = shorties.parent.parent.find_next_sibling('dd')
        shorties = shorties.get_text()
        if util.isValidFloat(shorties):
            return float(shorties)
        return 0

    
    # @params (None)
    # @descrip - finds the stocks % change value and parses it
    # @returns float -  either the value or None
    def get_percent_change(self) -> float:
        change = self.soup.find('span', class_='percent-change')
        change = change.get_text()
        change = change[2:(len(change) - 2)]      
        if util.isValidFloat(change):
            return float(change)
        return None


    # @params (None)
    # @descrip - finds the stocks actual price value and parses it
    # @returns float -  either the value or None
    def get_price(self) -> float:
        price = self.soup.find('dt', text="Closing Price")
        price = price.find_next_sibling('dd')
        price = price.get_text().replace(',','')
        if util.isValidFloat(price):
            return float(price)
        return None
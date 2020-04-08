#! /usr/bin/env python
# ====================== Gen Imports =========================
from bs4 import BeautifulSoup
import unicodedata
from datetime import datetime, timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import json
from math import floor

# ===================== Custom Imports =======================
import data_operations.utils.helpers as util
from shared.models import News_Event, Comp_Perfor_Sector, Comp_Perfor_Phys_Location

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
        sleep(1)  # Throttle all requests so we dont piss people off
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
    # @returns str - either BS4obj or the actual text
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
        self.news = [] # List of News Events
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
    # @descrip - finds the date of the last news article and checks to see if it was in the date ranges specified in utils. Also stores off news events.
    # @returns bool - true if we find a news article, false if not and stores off link,title and date into news field
    def has_finviz_news(self) -> bool:
        table = self.soup.find('table', id='news-table')
        table_rows = table.find_all('tr')

        for index, row in enumerate(table_rows):
            news_date = self.base.get_table_cell(row, 0, True)
            news_date = unicodedata.normalize('NFKD', news_date).strip()  # Drop Ending Bytes
            news_date = util.string_to_date(news_date)

            if (news_date != None):
                if index < 10:
                    for date in util.get_date_ranges():
                        if (news_date == date):
                            return True

                model = News_Event()
                title = self.base.get_table_cell(row, 1, False)
                title = title.find('a', href=True)
                model.data['date_of_article'] = news_date
                model.data['title_of_article'] = title.get_text()
                model.data['link'] = title['href']
                model.data['source'] = 'Finviz'
                self.news.append(model)
        return False


 # =========================================================== # 
 #                 SEC Edgar Files scraper                     #
 # ============================================================ #

class SEC_Edgar(Scaper):
    # when converting from ticker to CIK, cut list in half to see if our first
    # letter is before or after, then keep repeating unless python has a better
    # search option
    # keep going through page by page 100, until table is empty then we have reached the end of the form list

    # https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001113866&type=&dateb=&owner=exclude&start=0&count=100

    def __init__(self, ticker:str) -> None:
        self.base = super()
        self.cik = None
        self.soup = None
        self.is_valid_cik = self.get_cik(ticker) 
        return

    def get_cik(self, ticker:str) -> bool:
        with open('./data_operations/utils/cik_ticker.json') as f:
            cik_json = json.load(f)

        for cik_item in cik_json:
            if cik_json[cik_item]['ticker'] == ticker:
                self.cik = str(cik_json[cik_item]['cik_str'])
                return True
        return False


    #cik is a company/ticker/we
    def load_cik_data(self, increment: int) -> bool:
        # self.soup = self.base.get_data('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + self.cik + '&type=&dateb=&owner=exclude&start=0&count=100')
        self.soup = self.base.get_data('./cik-chu-' + str(increment) +'.html')
        if increment == 0:
            self.base_data = self.soup
        table = self.soup.find('table', class_='tableFile2')
        rows = table.find_all('tr')
        if len(rows) >= 2:
            return False
        
        return True


    # sic is all realated companies
    # returns a list of CIK numbers
    def get_sic_data(self, location_code: str, sic_code: str) -> list:
        # load and parse data here returning a list?
        inc = 0
        comps = []
        sic_html = self.base.get_data('./sic-chu-' + str(inc) + '.html')
        #sic_html = self.base.get_data('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=' + sic_code + '&owner=exclude&match=&start=' + str(inc) +'&count=100&hidefilings=0')

        while not sic_html.find('div', class_='noCompanyMatch'):
            table = sic_html.find('table', class_='tableFile2')
            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                if index == 0:  # Skip header TR row
                    continue

                comp_state_code = self.base.get_table_cell(row, 3, True)
                if location_code == comp_state_code:
                    comps.append(self.base.get_table_cell(row, 0, True))
                
            inc = inc + 100
            sic_html = self.base.get_data('./sic-chu-' + str(inc) + '.html')
            #sic_html = self.base.get_data('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=' + sic_code + '&owner=exclude&match=&start=' + str(inc) +'&count=100&hidefilings=0')

        return comps


    # call related companies after forms so we for sure have the base data
    def get_related_companies(self) -> list:
        #make sure to exclude the subject cik, it is included in the results
        # if related co not in CIK file, maybe they merged?
        # adr maybe different check up on it
        links = self.base_data.find('p', class_='identInfo')
        links = links.find_all('a', href=True)
        sic_code = links[0].get_text()
        location_code = links[1].get_text()
        company_ciks = self.get_sic_data(location_code, sic_code)
        # convert from cik to ticker here
        return


    def make_peer_performance_model(self, ticker:str) -> Comp_Perfor_Sector:
        # use yfinace to get ohlc data, custom roll percent change and populate a new model
        # load cik here
        ciks = self.get_related_companies()
        return


 # =========================================================== # 
 #                 TD Ameritrade scraper                        #
 # ============================================================ #

class TDAmeritrade(Scaper):

    # @params (ticker) - symbol to find, (index) = is the ticker a indice? 
    # @descrip - sets up a BS4 Obj webpage
    # @returns None
    def __init__(self, ticker: str, index=False):
        self.base = super()
        self.news = []
        if (index):
            self.soup = self.base.get_data('https://research.tdameritrade.com/grid/public/research/stocks/charts?symbol=' + ticker)
        else:
             # self.soup = self.base.get_data('https://research.tdameritrade.com/grid/public/research/stocks/summary?fromPage=overview&display=&fromSearch=true&symbol=' + ticker) 
            self.soup = self.base.get_data('../nostradamus_files/td-' + ticker + '.html')        
            return


    # @params (None)
    # @descrip - finds the date of the last news article and checks to see if it was in the date ranges specified in utils. If exception fires, assume there is no news.
    # @returns bool - Yes if TDAmeritrade has news, no if not
    def has_td_news(self) -> bool:
        table = self.soup.find('table', class_='latestNews')
        table_section = table.find_all('tbody')
        for index, tbody in enumerate(table_section):
            row = tbody.find_all('tr')
            news_date = util.string_to_date(row[0].get_text())
            if (news_date != None):
                if index < 10:
                    for date in util.get_date_ranges():
                        if (news_date == date):
                            return True
                
                model = News_Event()
                title = row[1]
                title = title.find('a', href=True)
                model.data['date_of_article'] = news_date
                model.data['title_of_article'] = title.get_text()
                model.data['link'] = title['href']
                model.data['source'] = 'TD Ameritrade'
                self.news.append(model)
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
        change = self.soup.find_all('span', class_='percent-change')
        # if we have after hours action, we need to get the days close not the afterhours
        change = change[len(change) - 1]
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


    # @params (None)
    # @descrip - looks for ADR tag to indicate this a ADR
    # @returns bool - yes its an adr or no its not
    def get_adr(self) -> bool:
        adr = self.soup.find_all('div', class_='adr-container')
        if len(adr) > 0:
            return True
        return False
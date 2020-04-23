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
import yfinance
from os import path

# ===================== Custom Imports =======================
import data_operations.utils.helpers as util
from shared.models import News_Event, Peer_Performance, SEC, SEC_Company_Info, SEC_Employee_Stock, SEC_Merger, SEC_Secondary_Offering


with open('../data_operations/config.json') as f:
            config = json.load(f)


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
                browser = webdriver.Firefox(executable_path=config['project_root'] + '.venv/lib/geckodriver',options=options)
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
            change = change.replace('%','').replace('-', '')
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
        if table == None:
            return False

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

    # @params (ticker) - ticker => company we want to gather info on. 
    # @descrip - Set ups required fields for class use. if we can find info from the ticker, then try to find it from the CIK number.
    # @returns None
    def __init__(self, ticker:str) -> None:
        self.base = super()
        self.ticker = ticker
        self.base_data = self.base.get_data('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + ticker + '&type=&dateb=&owner=exclude&start=0&count=100')
        self.cik = None
        self.cik_dict = {}
        self.soup = None
        self.is_valid = True
        self.links_s8 = []
        self.links_425 = []
        self.links_s3 = []
        self.links_8k = []
        self.links_f3 = []
        self.links_f6 = []
        self.links_f4 = []
        self.late_filings = 0
        self.ct_orders = 0
        self.ipo_date = datetime.today().date()
        self.is_adr = False
        
        with open('../data_operations/utils/cik_ticker.json') as f:
            self.cik_dict = json.load(f)

        if self.base_data.find('h1', text="No matching Ticker Symbol."):
            self.is_valid = False

        cik = base_data.find('span', class_='companyName')
        cik = cik.find('a').get_text()
        self.cik = cik.split(' ')[0]

        return


    # @params (inc) - inc => determines which "page" we are on since SEC maxium display count is 100.
    # @descrip - Makes the request, and scrapes the given page.
    # @returns bool - true if we have data, false if we at the end of line.
    def load_data(self, inc: int) -> bool:
        self.soup = self.base.get_data('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + self.ticker + '&type=&dateb=&owner=exclude&start=' + str(inc) + '&count=100')
        table = self.soup.find('table', class_='tableFile2')
        rows = table.find_all('tr')
        if len(rows) >= 2:
            return True
        
        return False


    # @params (location_code, sic_code) - loc_code => the state in which the company is registerd (a SEC code) / sic_code => the sector in which the company is registered (SEC code) 
    # @descrip - loads the company search by SIC code, and cross references by location code
    # @returns list - a list of CIK codes of companies in the same state, and same sector.
    def get_sic_data(self, location_code: str, sic_code: str) -> list:
        inc = 0
        comps = []
        sic_html = self.base.get_data('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=' + sic_code + '&owner=exclude&match=&start=' + str(inc) +'&count=100&hidefilings=0')

        while not sic_html.find('div', class_='noCompanyMatch'):
            table = sic_html.find('table', class_='tableFile2')
            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                if index == 0:  # Skip header TR row
                    continue

                comp_state_code = self.base.get_table_cell(row, 2, True)
                if location_code == comp_state_code:
                    comps.append(self.base.get_table_cell(row, 0, True))
                
            inc = inc + 100
            sic_html = self.base.get_data('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=' + sic_code + '&owner=exclude&match=&start=' + str(inc) +'&count=100&hidefilings=0')

        return comps


    # @params (None) 
    # @descrip - iterates through list of CIKs and converts to a ticker str
    # @returns list - a list of ticker str's of companies in the same state and same sector.
    def get_related_companies(self) -> list:
        # if related co not in CIK file, maybe they merged?
        related_cos = []
        links = self.base_data.find('p', class_='identInfo')
        links = links.find_all('a', href=True)
        sic_code = links[0].get_text()
        location_code = links[1].get_text()
        company_ciks = self.get_sic_data(location_code, sic_code)
        for cik in company_ciks:
            for cik_item in self.cik_dict:
                if str(self.cik_dict[cik_item]['cik_str']) in cik and cik != self.cik:
                    related_cos.append(self.cik_dict[cik_item]['ticker'])
                    break
        return related_cos


    # @params (ticker) - ticker of competeing company
    # @descrip - Takes a specified ticker and collects the past 5 days price action for it 
    # @returns list - a list of peer_performance models for each day we have data
    def make_arr_peer_performance_model(self, ticker:str) -> list:
        sleep(1) # Yfinance rate limiting
        peer_list = []
        symbol = yfinance.Ticker(ticker)

        data = symbol.history(period='5d')
        for index,row in data.iterrows():
            try:
                peer_model = Peer_Performance()
                peer_model.data['ticker'] = ticker
                peer_model.data['date'] = index.date()
                peer_model.data['open'] = row.Open
                peer_model.data['high'] = row.High
                peer_model.data['low'] = row.Low
                peer_model.data['close'] = row.Close
                peer_model.data['volume'] = row.Volume
                peer_model.data['percent_change'] = peer_model.to_percent(row.Open, row.Close)
                peer_list.append(peer_model)
            except:
                # Not valid ticker or whatever. Dont add the model.
                pass
        
        return peer_list


    # @params (None) 
    # @descrip - Iterates through the filings page by page and pulls out the forms we are looking for. Only for american listed companies which have different reporting requirments.
    # @returns None
    def parse_sec_filings(self) -> None:
        inc = 0
        s1_found = False
        while self.load_data(inc):
            table = self.soup.find('table', class_='tableFile2')
            rows = table.find_all('tr')
            if self.is_adr:
                self.parse_sec_foreign_filings(table)
            else:
                for index, row in enumerate(rows):
                    if index == 0:  # Skip header row
                        continue

                    form_id = self.base.get_table_cell(row, 0, True)

                    if form_id == '6-K' or form_id == 'F-1' or form_id == 'F-3' or form_id == 'F-6' or form_id == 'F-3ASR' or form_id == '20-F':
                        # Safe to say this is a ADR 
                        self.is_adr = True
                        self.parse_sec_foreign_filings(table)
                        break
                    elif form_id == 'NT 10-K' or form_id == 'NT 10-Q' or form_id == 'NT 10-D' or form_id == 'NT 11-k':
                        self.late_filings += 1
                    elif form_id == 'S-8':
                        link = self.base.get_table_cell(row, 1, False)
                        link = link.find('a', href=True)
                        self.links_s8.append('https://www.sec.gov' + link['href'])
                    elif form_id == 'S-3' or form_id == 'S-3ASR':
                        link = self.base.get_table_cell(row, 1, False)
                        link = link.find('a', href=True)
                        self.links_s3.append('https://www.sec.gov' + link['href'])
                    elif form_id == 'CT ORDER':
                        self.ct_orders += 1
                    elif form_id == '8-K':
                        link = self.base.get_table_cell(row, 1, False)
                        link = link.find('a', href=True)
                        self.links_8k.append('https://www.sec.gov' + link['href'])
                    elif form_id == 'S-1':
                        s1_found = True
                        self.ipo_date = self.base.get_table_cell(row, 3, True)
                    elif form_id == '425':
                        link = self.base.get_table_cell(row, 1, False)
                        link = link.find('a', href=True)
                        self.links_425.append('https://www.sec.gov' + link['href'])

            if not s1_found:
                last_parsed_date = self.base.get_table_cell(rows[(len(rows) - 1)], 3, True)
                if util.string_to_date(last_parsed_date) != None:
                    if self.ipo_date > util.string_to_date(last_parsed_date):
                            self.ipo_date = util.string_to_date(last_parsed_date)

            inc += 100
        return


    # @params (None) 
    # @descrip - Iterates through the filings page by page and pulls out the forms we are looking for. Only for foreign listed companies which have different reporting requirments.
    # @returns None
    def parse_sec_foreign_filings(self, sec_table) -> None:
        # 6K can contain just too much disorganized information. Skipping for now.
        rows = sec_table.find_all('tr')

        # Since Foreign issuers dont have to file a S-1, just find the first entry
        last_parsed_date = self.base.get_table_cell(rows[(len(rows) - 1)], 3, True)
        if util.string_to_date(last_parsed_date) != None:
            if self.ipo_date > util.string_to_date(last_parsed_date):
                            self.ipo_date = util.string_to_date(last_parsed_date)

        for index, row in enumerate(rows):
                last_parsed_date = None
                if index == 0:  # Skip header row
                    continue

                form_id = self.base.get_table_cell(row, 0, True)

                if form_id == 'NT 11-k' or form_id == 'NT 20-F' or form_id == 'NT 10-D':
                    self.late_filings += 1
                elif form_id == 'F-4':
                    link = self.base.get_table_cell(row, 1, False)
                    link = link.find('a', href=True)
                    self.links_f4.append('https://www.sec.gov' + link['href'])
                elif form_id == 'F-3' or form_id == 'F-3ASR':
                    link = self.base.get_table_cell(row, 1, False)
                    link = link.find('a', href=True)
                    self.links_f3.append('https://www.sec.gov' + link['href'])
                elif form_id == 'CT ORDER':
                    self.ct_orders += 1
                elif form_id == 'S-8':
                    link = self.base.get_table_cell(row, 1, False)
                    link = link.find('a', href=True)
                    self.links_s8.append('https://www.sec.gov' + link['href'])
                elif form_id == 'S-3' or form_id == 'S-3ASR':
                    link = self.base.get_table_cell(row, 1, False)
                    link = link.find('a', href=True)
                    self.links_s3.append('https://www.sec.gov' + link['href'])
                elif form_id == 'F-6':
                    link = self.base.get_table_cell(row, 1, False)
                    link = link.find('a', href=True)
                    self.links_f6.append('https://www.sec.gov' + link['href'])
                elif form_id == '425':
                    link = self.base.get_table_cell(row, 1, False)
                    link = link.find('a', href=True)
                    self.links_425.append('https://www.sec.gov' + link['href'])
        return


    # @params (None) 
    # @descrip - iterate though our forms we want, and scrapes each page trying to find the necessary information.
    # @returns SEC model with all information
    def make_sec_model(self) -> SEC:
        self.parse_sec_filings()
        model = SEC()
        model.data['date_of_ipo'] = self.ipo_date
        model.data['late_filings'] = self.late_filings
        model.data['ct_orders'] = self.ct_orders
        model.data['is_adr'] = self.is_adr
        
        # ====================== American Company =========================

        for link in self.links_s3:
            offering_model = self.make_secondary_offering_model(link)
            if offering_model.data['date'] != None:
                model.data['secondary_offerings'].append(offering_model)
        
        for link in self.links_8k:
            info_model = self.make_company_info_model(link)
            model.data['company_info'].append(info_model)

        # ======================== Foreign Company ===========================

        for link in self.links_f3:
            offering_model = self.make_secondary_offering_model(link)
            if offering_model.data['date'] != None:
                model.data['secondary_offerings'].append(offering_model)

        for link in self.links_f4:
            offering_model = self.make_secondary_offering_model(link)
            if offering_model.data['date'] != None:
                model.data['secondary_offerings'].append(offering_model)

        for link in self.links_f6:
            offering_model = self.make_secondary_offering_model(link)
            if offering_model.data['date'] != None:
                model.data['secondary_offerings'].append(offering_model)

        # ======================== Applies to both ======================

        for link in self.links_s8:
            stock_prog_model = self.make_stock_program_model(link)
            if stock_prog_model.data['date'] != None:
                model.data['stock_program'].append(stock_prog_model)

        for link in self.links_425:
            merger_model = self.make_merger_model(link)
            same_mergering_co = False
            
            for mergering_co in model.data['mergers']:
                if merger_model.data['merging_with_cik'] == None or merger_model.data['merging_with_cik'] == mergering_co.data['merging_with_cik']:
                    same_mergering_co = True
                    break

            if not same_mergering_co:
                model.data['mergers'].append(merger_model)

        return model


    # @params (link) - a link to form index page (Not the actual form)
    # @descrip - navigates to the form and tries to find the table that specifies how many shares were issued.
    # @returns SEC_Secondary_Offering Model
    def make_secondary_offering_model(self, link: str) -> SEC_Secondary_Offering:
        model = SEC_Secondary_Offering()
        model.data['link'] = link
        try:
            issued_shares = None
            model.data['is_asr'] = False
            data = self.base.get_data(link)
            # Get date from info header
            submission_date = data.find('div', text='Filing Date')
            submission_date = submission_date.find_next_sibling('div')
            model.data['date'] = submission_date.get_text()
            # parse main table for form type and link to actual submission
            table = data.find('table', class_='tableFile')
            rows = table.find_all('tr')
            form_type = self.base.get_table_cell(rows[1], 3, True)
            form = self.base.get_table_cell(rows[1], 2, False)
            form = form.find('a', href=True)
            form = 'https://www.sec.gov' + form['href']

            if form_type == 'S-3ASR':
                model.data['is_asr'] = True

            if path.splitext(form)[1] == '.txt':
                # Currently, we dont parse text files.
                # Usually means its from over 15 years ago.
                # Null Date so we dont append
                model.data['date'] = None
                return model

            # Parse the actual submission form for information
            data = self.base.get_data(form)
            stock_offering_table_rows = None
            tables = data.find_all('table')

            for table in tables:
                try:
                    rows = table.find_all('tr')
                    title_cell = self.base.get_table_cell(rows[2], 0, True)
                    title_cell = title_cell.lstrip()
                    if 'Title of ' in title_cell:
                        stock_offering_table_rows = rows
                        break
                except:
                    # Who the eff knows what table this is, but pass
                    continue

            # If its a standard table, try to get where we initially think the issued shares should be then clean it up
            issued_shares = self.base.get_table_cell(stock_offering_table_rows[3], 2, True)
            issued_shares = unicodedata.normalize('NFKD', issued_shares)
            issued_shares = issued_shares.split(' America')[0].replace(',', '').replace('shares','').strip()

            if util.isValidInt(issued_shares):
                model.data['additional_shares_issued'] = int(issued_shares) 
                return model

            # Although Common Stock is in the table twice, we are not breaking. So our "issued shares" is the last occurance of title "common stock"
            for row in stock_offering_table_rows:
                row_title = self.base.get_table_cell(row, 0, True).split(',')[0].split('(')[0].strip()
                if row_title.lower() == 'common stock':
                    issued_shares = self.base.get_table_cell(row, 2, True).split(' Amercia')[0].replace(',','').split(' shares')[0].split('(')[0]

            # if we parsed the wrong row, oh well, null it out
            model.data['additional_shares_issued'] = int(issued_shares) if util.isValidInt(issued_shares) else None

            return model
        except:
            # if we blow up just add the link for future reference
            return model


    # @params (link) - a link to form index page (Not the actual form)
    # @descrip - Checks the blue info boxes for the companies that received notification from letters. We are assuming that because the companies have been notified that a merger is taking place. Other options are: Merger failed, Company bought a product from another company etc.
    # @returns SEC_Merger Model
    def make_merger_model(self, link: str) -> SEC_Merger:
        model = SEC_Merger()
        merging_cik = None
        merging_name = None
        try:
            data = self.base.get_data(link)
            # Get date from info header
            submission_date = data.find('div', text='Filing Date')
            submission_date = submission_date.find_next_sibling('div').get_text()
            model.data['date'] = submission_date

            companies = data.find_all('span', class_='companyName')
            for company in companies:
                cik = company.find('a').get_text()
                cik = cik.split(' ')[0]

                if self.cik in cik:
                    continue
                
                merging_cik = cik
                merging_name = company.get_text().split(' (')[0]

            model.data['merging_with_company'] = merging_name
            model.data['merging_with_cik'] = merging_cik
            model.data['date'] = submission_date
        except:
            # Dont append to our main model because our cik is null
            model.data['merging_with_cik'] = None
        finally:
            return model


    # @params (link) - a link to form index page (Not the actual form)
    # @descrip - Looks at the header information to find the different sections that the 8-k is reporting on. For more detail, we will have to use the link to view the 8-k ourselves.
    # @returns SEC_Company_Info
    def make_company_info_model(self, link: str) -> SEC_Company_Info:
        model = SEC_Company_Info()
        model.data['link'] = link
        try:
            data = self.base.get_data(link)
            table = data.find('table', class_='tableFile')
            rows = table.find_all('tr')

            submission_date = data.find('div', text='Filing Date')
            submission_date = submission_date.find_next_sibling('div').get_text()

            item_group = data.find('div', text='Items').parent
            item_group = item_group.find('div', class_='info')
            item_group = item_group.get_text(separator='|').split('|')
            for item in item_group:
                item_details = item.split(': ')
                item_num = item_details[0].split('Item ')[1]
                model.data['item_list'][item_num] = item_details[1]

            model.data['date'] = submission_date
            form_link = self.base.get_table_cell(rows[1], 2, False)
            form_link = form_link.find('a', href=True)
            model.data['link'] = 'https://www.sec.gov' + form_link['href']
        except:
            # Just save off the link
            pass
        finally:
            return model


    # @params (link) - a link to form index page (Not the actual form)
    # @descrip - navigates to the form and tries to find the table that specifies how many shares were issued for employee benefits. Although they are issuing more shares, it means the employees are invested in the co.
    # @returns SEC_Employee_Stock
    def make_stock_program_model(self, link: str) -> SEC_Employee_Stock:
        model = SEC_Employee_Stock()
        model.data['link'] = link
        try:
            issued_shares = None
            data = self.base.get_data(link)
            # Get date from info header
            submission_date = data.find('div', text='Filing Date')
            submission_date = submission_date.find_next_sibling('div')
            model.data['date'] = submission_date.get_text()
            # parse main table for form type and link to actual submission
            table = data.find('table', class_='tableFile')
            rows = table.find_all('tr')
            form = self.base.get_table_cell(rows[1], 2, False)
            form = form.find('a', href=True)
            form = 'https://www.sec.gov' + form['href']

            if path.splitext(form)[1] == '.txt':
                # Currently, we dont parse text files.
                # Usually means its from over 15 years ago.
                # Null Date so we dont append
                model.data['date'] = None
                return model

            # Parse the actual submission form for information
            data = self.base.get_data(form)
            stock_offering_table_rows = None
            tables = data.find_all('table')

            for table in tables:
                try:
                    rows = table.find_all('tr')
                    title_cell = self.base.get_table_cell(rows[2], 0, True)
                    title_cell = title_cell.lstrip()
                    if 'Title of ' in title_cell:
                        stock_offering_table_rows = rows
                        break
                except:
                    # Who the eff knows what table this is, but pass
                    continue

            # If its a standard table, try to get where we initial think the issued shares should be then clean it up
            issued_shares = self.base.get_table_cell(stock_offering_table_rows[3], 2, True)
            issued_shares = unicodedata.normalize('NFKD', issued_shares)
            issued_shares = issued_shares.split(' America')[0].replace(',', '').replace('shares','').strip()

            if util.isValidInt(issued_shares):
                model.data['additional_shares_issued'] = int(issued_shares) 
                return model

            # Although Common Stock is in the table twice, we are not breaking. So our "issued shares" is the last occurance of title "common stock"
            for row in stock_offering_table_rows:
                row_title = self.base.get_table_cell(row, 0, True).split(',')[0].split('(')[0].strip()
                if row_title.lower() == 'common stock':
                    issued_shares = self.base.get_table_cell(row, 2, True).split(' America')[0].replace(',','').split(' shares')[0].split('(')[0]

            # if we parsed the wrong row, oh well, null it out
            model.data['additional_shares_issued'] = int(issued_shares) if util.isValidInt(issued_shares) else None

        except:
            # if we blow up just add the link for future reference
            pass
        finally:
            return model




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
            self.soup = self.base.get_data('https://research.tdameritrade.com/grid/public/research/stocks/summary?fromPage=overview&display=&fromSearch=true&symbol=' + ticker)      
        return


    # @params (None)
    # @descrip - finds the date of the last news article and checks to see if it was in the date ranges specified in utils. If exception fires, assume there is no news.
    # @returns bool - Yes if TDAmeritrade has news, no if not
    def has_td_news(self) -> bool:
        table = self.soup.find('table', class_='latestNews')
        if table == None:
            return False

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
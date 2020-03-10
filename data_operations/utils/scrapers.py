import data_operations.utils.helpers as util
from bs4 import BeautifulSoup
import unicodedata
from datetime import datetime, timedelta



 # ======================================================= # 
 #            Bloomberg scraper                            #
 # ======================================================= #


class Bloomberg(util.Scaper):

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



 # ======================================================= # 
 #            Finviz scraper                               #
 # ======================================================= #


class FinViz(util.Scaper):
    
    def __init__(self, path: str):
        self.base = super()
        self.soup = self.base.get_data(path)
        return
    

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


    def get_last_finviz_row_id(self) -> int:
        table_rows = self.table.find_all('tr')
        for row in table_rows:
            last_id = self.base.get_table_cell(row, 0, True)
            if (util.isValidInt(last_id)):
                last_id = int(last_id)
        return last_id


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


 # ======================================================= # 
 #            TD Ameritrade scraper                        #
 # ======================================================= #


class TDAmeritrade(util.Scaper):

    def __init__(self, ticker: str):
        self.base = super()
        # self.soup = self.base.get_data('https://research.tdameritrade.com/grid/public/research/stocks/summary?fromPage=overview&display=&fromSearch=true&symbol=' + ticker)
        self.soup = self.base.get_data('../nostradamus_files/td-' + ticker + '.html')
        return


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


    def get_sector(self) -> str:
        # keep in mind this for the current day of gaining 10%. We need the previous days because the current means nothing to us.
        sector = self.soup.find('div', class_='company-detail-information')
        sector = sector.get_text().split(':') 
        sector = unicodedata.normalize('NFKD', sector[0]).strip()       
        return sector.lower()

    
    def get_shares_outstanding(self) -> int:
        shares_outstanding = self.soup.find('dt', text="Shares Outstanding")
        shares_outstanding = shares_outstanding.find_next_sibling('dd')
        return util.string_to_int_abbv(shares_outstanding.get_text())


    def get_tute_ownership(self) -> float:
        tutes = self.soup.find('a', text="% Held by Institutions")
        tutes = tutes.parent.parent.find_next_sibling('dd')
        if util.isValidFloat(tutes.get_text()):
            return float(tutes.get_text())
        return 0


    def get_short_intrest(self) -> float:
        shorties = self.soup.find('a', text="Short Interest")
        shorties = shorties.parent.parent.find_next_sibling('dd')
        if util.isValidFloat(shorties.get_text()):
            return float(shorties.get_text())
        return 0


    
import utils.helpers as util
from bs4 import BeautifulSoup



 # ======================================================= # 
 #            Bloomberg scraper                            #
 # ======================================================= #


class Bloomberg(Singleton, Scaper):

    def __init__(self, ticker):
        # scrape here, singleton class, and maintain state of array of arrays %gains
        self.base = super()
        self.ticker = ticker
        return

    def get_sector_performance(self, sector):
        # 
        return


 # ======================================================= # 
 #            Finviz scraper                               #
 # ======================================================= #


class FinViz(Scaper):
    
    def __init__(self):
        self.base = super()
        return
    
    def get_tickers(self):
        # call get data incrementing path by 20 ( starting at 21)
        tickers = []
        soup = self.base.get_data('../finviz.html')
        table = soup.find('table', attrs={'bgcolor': '#d3d3d3', 'border': '0', 'cellpadding': '3', 'cellspacing': '1', 'width': '100%'})
        table_rows = table.find_all('tr')
        for row in table_rows:
            change = self.base.get_table_cell(row, 9, True)
            print(util.isValidFloat(change[:-1]))

    def has_finviz_news(self):
        table = self.soup.find('table', id='news-table')
        table_rows = table.find_all('tr')
        for row in table_rows:
            latest_news_date = self.base.get_table_cell(row, 0, True)
            latest_news_date = util.string_to_date(latest_news_date)

            if (latest_news_date != None and latest_news_date == util.current_date()):
                return True
        return False


 # ======================================================= # 
 #            Naked Short Report scraper                   #
 # ======================================================= #


class Naked_Short_Report(Scaper):

    def __init__(self, ticker):
        # scrape here, singleton class, and maintain state of array of arrays %gains
        self.base = super()
        self.ticker = ticker
        return


 # ======================================================= # 
 #            Nasdaq scraper                               #
 # ======================================================= #


class Nasdaq(Scaper):

    def __init__(self, ticker):
        # scrape here, singleton class, and maintain state of array of arrays %gains
        self.base = super()
        self.ticker = ticker
        return


 # ======================================================= # 
 #            TD Ameritrade scraper                        #
 # ======================================================= #


class TDAmeritrade(Scaper):

    def __init__(self, ticker):
        self.base = super()
        # self.soup = self.base.get_data('https://research.tdameritrade.com/grid/public/research/stocks/summary?fromPage=overview&display=&fromSearch=true&symbol=' + ticker)
        return

    def has_td_news(self):
        table = self.soup.find('table', class_='latestNews')
        table_section = table.find_all('tbody')
        lastest_news_date = table_section[0].find('tr > th')
        if (lastest_news_date != None):
            lastest_news_date = lastest_news_date.get_text()
            lastest_news_date = util.string_to_date(lastest_news_date)
            if (lastest_news_date != None and lastest_news_date == util.current_date()):
                return True
        return False

    def get_sector(self):
        sector = self.soup.find(class_='company-detail-container > company-detail-information').get_text()
        return sector

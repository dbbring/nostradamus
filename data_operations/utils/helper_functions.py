from bs4 import BeautifulSoup
import os
import copy

class FinViz(object):
    
    def __init__(self):
        return
    
    def get_tickers(self):
        # call get data incrementing path by 20 ( starting at 21)
        tickers = []
        soup = BeautifulSoup(self.get_data('path'), 'html.parser')
        table = soup.find('div', id='screener-content')
        table_rows = table.contents[1].find_all('tr')
        for row in table_rows:
            change = self.disect_table_row(row, 8)
            #print(change)

    def get_data(self, path):
        dummy_html = open('../finviz.html', encoding='utf-8')
        return dummy_html

    # @returns value of specified cell
    def disect_table_row(self, row, column):
        table_cells = row.contents
        for cell in table_cells:
            for i in range(0, column):
                cellContents = cell
        return cellContents
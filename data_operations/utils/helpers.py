from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
 
# Date ranges to check for a news event. Today plus 3 days ago.
def get_date_ranges() -> list:
    today = datetime.today()
    one_day_ago = (today - timedelta(days=1))
    two_days_ago = (today - timedelta(days=2))
    three_days_ago = (today - timedelta(days=3))
    return [today.date(), one_day_ago.date(), two_days_ago.date(), three_days_ago.date()]

def isValidFloat(str: str) -> bool:
    try: 
        float(str)
        return True
    except ValueError:
            return False

def isValidInt(str: str) -> bool:
    try: 
        int(str)
        return True
    except ValueError:
            return False

def string_to_date(date_string: str) -> datetime:
    if (date_string == None):
        return date_string

    # Format must be June 1, 2005.
    try:
        dateObj = datetime.strptime(date_string, '%B %d, %Y').date()
    except ValueError:
        # Format must be Feb-17-20 07:07AM
        try:
            dateObj = datetime.strptime(date_string, '%b-%d-%y %I:%M%p').date()
        except ValueError:
            dateObj = None
            
    return dateObj


def string_to_int_abbv(strToConvert: str) -> int:
    # Cast to float because of decmial point. (126.60M) then int for whole number.
    try:
        return float(strToConvert)
    except ValueError:
        last_letter = strToConvert[len(strToConvert) - 1:]
        int_only = strToConvert[:len(strToConvert) - 1]
        if last_letter.upper() == 'B':
            return int(float(int_only) * 1000000000)
        elif last_letter.upper() == 'M':
            return int(float(int_only) * 1000000)
        elif last_letter.upper() == 'K':
            return int(float(int_only) * 1000)
        else:
            return 0


 # ======================================================= # 
 #            Abstract Classes                             #
 # ======================================================= #


class Base_Model(object):


     def __init__(self):
         # Just a number that is way outside the normal range so we can instaniate an property 
         self.initial_float = 999999.99
         return


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class API_Request(object):
    
    def __init__(self):
        return

    def get_request(self, _url):
        r = requests.get(url=_url)
        return r.json()


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class Scaper(object):
    
    def __init__(self):
        return

    def get_data(self, path: str) -> BeautifulSoup:
        try:
            html = open(path, encoding='utf-8')
        except:
            options = Options()
            options.headless = True
            browser = webdriver.Firefox(executable_path='/home/derek/Desktop/nostradamus/.venv/lib/geckodriver',options=options)
            browser.get(path)
            html = browser.page_source
            browser.close()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    # @returns value of specified cell or cell html contents
    def get_table_cell(self, row, column, get_text):
        table_cells = row.find_all('td')
        if get_text:
            return table_cells[column].get_text()
        return table_cells[column]



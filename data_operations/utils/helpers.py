from bs4 import BeautifulSoup
from datetime import datetime, date

def current_date():
    return date.today()

def isValidFloat(str):
    try: 
        float(str)
        return True
    except ValueError:
            return False

def string_to_date(date_string):
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


 # ======================================================= # 
 #            Abstract Classes                             #
 # ======================================================= #


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class API_Request(object):
    
    def __init__(self):
        return


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class Scaper(object):
    
    def __init__(self):
        return

    def get_data(self, path):
        dummy_html = open(path, encoding='utf-8')
        soup = BeautifulSoup(dummy_html, 'html.parser')
        return soup

    # @returns value of specified cell or cell html contents
    def get_table_cell(self, row, column, get_text):
        table_cells = row.find_all('td')
        if get_text:
            return table_cells[column].get_text()
        return table_cells[column]


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


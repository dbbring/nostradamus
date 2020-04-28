#! /usr/bin/env python
# ======================= Gen Imports ========================
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# ===================== Custom Imports ========================


# @params (None)
# @descrip - Date ranges to check for a news event. Today plus 3 days ago.
# @returns list - list of date objs that today,yesterday,two days and three days ago.
def get_date_ranges() -> list:
    today = datetime.today()
    one_day_ago = (today - timedelta(days=1))
    two_days_ago = (today - timedelta(days=2))
    three_days_ago = (today - timedelta(days=3))
    return [today.date(), one_day_ago.date(), two_days_ago.date(), three_days_ago.date()]


# @params (str) - str representation of float value
# @descrip - trys to convert str to float
# @returns bool - true if the string is a valid float, false if not
def isValidFloat(str: str) -> bool:
    try: 
        float(str)
        return True
    except ValueError:
            return False


# @params (str) - str representation of int value
# @descrip - trys to convert to str to an int
# @returns bool - true if str is valid int, false if not
def isValidInt(str: str) -> bool:
    try: 
        int(str)
        return True
    except ValueError:
            return False


# @params (str) - str representation of a date
# @descrip - tries to convert various dates into date obj.
# @returns datetime - None if we cant convert, otherwise returns datetime of the string.
def string_to_date(date_string: str) -> datetime:
    if (date_string == None):
        return None

    # Format must be June 1, 2005.
    try:
        dateObj = datetime.strptime(date_string, '%B %d, %Y').date()
    except ValueError:
        # Format must be Feb-17-20 07:07AM
        try:
            dateObj = datetime.strptime(date_string, '%b-%d-%y %I:%M%p').date()
        except ValueError:
            # Format must be 2020-02-17
            try:
                dateObj = datetime.strptime(date_string, '%Y-%m-%d').date()
            except ValueError:
                dateObj = None
            
    return dateObj


# @params (strToConvert) - a string representation of roman numeral number. ex. 126.60M
# @descrip - converts thous, mill, and bill str values into a int
# @returns int - int value of str
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



# ============================================================ # 
#                  FireFox Browser Instance                    #
# ============================================================ #

class FireFox(object):

    # @params (cls) class instance
    # @descrip - either returns the current instance or a new instance
    # @returns one and only instance
    def __new__(cls):
      if not hasattr(cls, 'instance'):
          cls.instance = super(FireFox, cls).__new__(cls)
      return cls.instance


    # @params (None)
    # @descrip - MUST SET CONFIG BEFORE USE!
    # @returns None
    def __init__(self) -> None:
      self.browser = None
      self.config = None
      return


    # @params (None) 
    # @descrip - gets the current browser 
    # @returns None
    def start_browser(self) -> None:
      if self.config is None:
        return

      if self.browser is None:
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(executable_path=self.config['project_root'] + '.venv/lib/geckodriver',options=options)
      return


    # @params (path) a url to navigate to
    # @descrip - gets the HTML source from the specified url
    # @returns str - the html source code
    def get_html(self, path: str) -> str:
      self.start_browser()
      self.browser.get(path)
      return self.browser.page_source


    # @params (None)
    # @descrip - Shuts down the browser on desconstruction
    # @returns None
    def __del__(self) -> None:
      self.browser.close()
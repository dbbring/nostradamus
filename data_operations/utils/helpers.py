from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
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

def send_mail(message: str) -> None:
    gmailUser = 'nostradamus.notifications@gmail.com'
    gmailPassword = 'gatoradegreengrass'
    recipient = 'dev.dbbring@gmail.com'
    email_message=message

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = "-- | Nostradamus Update | --"
    msg.attach(MIMEText(email_message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()


 # ======================================================= # 
 #            Abstract Classes                             #
 # ======================================================= #


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

    # @returns value of specified cell or cell html contents
    def get_table_cell(self, row, column, get_text):
        table_cells = row.find_all('td')
        if get_text:
            return table_cells[column].get_text()
        return table_cells[column]



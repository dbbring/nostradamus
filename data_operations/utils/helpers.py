#! /usr/bin/env python
# ======================= Gen Imports ========================
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# ===================== Custom Imports ========================
from data_operations.database.helpers import DB
from data_operations.utils.api_requests import AlphaVantage, IEX
from shared.models import Ticker


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


# @params (db_name, TD, ticker, sp_inputs) - db_name, which instance of db to use - TD, TdAmeritrade object since we already have it when we call this. ticker, current ticker in iteration. s_p inputs, the dict of sp values for tech model.
# @descrip - Main function that gets spun off into different threads. Its here because we need sleep for 30 secs for Alphavantage rate limiting before we spin off.
# @returns None 
def process_ticker(db_name:str, TD, FinViz, ticker: str, s_p_inputs: dict) -> None:
    try:
        db = DB(db_name)
        company = Ticker()
        company.basic_info.data['ticker'] = ticker
        company.basic_info.data['date'] = datetime.now().date()
        company.basic_info.data['percent_change'] = TD.get_percent_change()
        sectors = TD.get_sector()

        symbol = AlphaVantage(ticker)
        symbol_wk = AlphaVantage(ticker, False)
        inputs = symbol.get_inputs()
        wk_inputs = symbol_wk.get_inputs()
        inputs['s_p'] = s_p_inputs['close']

        # stop each array after x number of days we dont need the whole thing
        start = len(inputs['date']) - 1
        end = start - 5
        
        for index in range(start, end, -1):
            wk_data = symbol_wk.make_price_wk_model(wk_inputs, index)
            company.weekly.append(wk_data)

            eod_data = symbol.make_price_eod_model(inputs, index)
            company.eod.append(eod_data)

            tech_data = symbol.make_tech_indic_model(inputs, index)
            company.tech_anaylsis.append(tech_data)

            chart_data = symbol.make_chart_idic_model(inputs, index)
            company.chart_anaylsis.append(chart_data)

        fa = IEX(ticker)
        fa_data = fa.make_fund_indic_model(inputs)
        fa_data.data['sector'] = sectors['top-level']
        fa_data.data['sub_sector'] = sectors['second-level']
        fa_data.data['institutional_ownership'] = TD.get_tute_ownership()
        fa_data.data['short_interest_percent'] = TD.get_short_intrest()
        fa_data.data['is_adr'] = TD.get_adr()

        company.fund_anaylsis = fa_data

        company.news = company.news + FinViz.news
        company.news = company.news + TD.news

        # SEC get similiar sector cos, and locational cos
        # Make Comp_Sector and Comp_Phys_loca Models
        # Keep with the trend, have SEC do a model factory
        # Append cos to company.comp_sector, and company.comp_geo
        # SEC get forms

        db.save_ticker_model(company)
        return
    except Exception as err:
        print(repr(err))
        # if whatever reason we fail, dont bother saving
        pass


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


# @params (message) the body of the email
# @descrip - uses disposable email account to send updates
# @returns None 
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



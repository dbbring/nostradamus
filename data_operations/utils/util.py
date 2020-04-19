#! /usr/bin/env python
# ======================= Gen Imports ========================
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# ===================== Custom Imports ========================
from data_operations.database.helpers import DB
from data_operations.utils.scrapers import SEC_Edgar
from data_operations.utils.api_requests import AlphaVantage, IEX
from shared.models import Ticker, SEC, Peer_Performance, SEC_Company_Info, SEC_Employee_Stock, SEC_Merger, SEC_Secondary_Offering




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

    company.fund_anaylsis = fa_data

    company.news = company.news + FinViz.news
    company.news = company.news + TD.news
  
    sec = SEC_Edgar(ticker)
    if sec.is_valid:
        sec_data = sec.make_sec_model()

        comps = sec.get_related_companies()
        for ticker in comps:
            p_p = sec.make_arr_peer_performance_model(ticker)
            company.peers = company.peers + p_p

    company.sec = sec_data
    
    db.save_ticker_model(company)
    return

  except Exception:
    # if whatever reason we fail, dont bother saving corrupt data
    pass



# @params (message) the body of the email
# @descrip - uses disposable email account to send updates
# @returns None 
def send_mail(message: str, db_name: str) -> None:
    gmailUser = 'nostradamus.notifications@gmail.com'
    gmailPassword = 'gatoradegreengrass'
    recipient = 'dev.dbbring@gmail.com'
    email_message=message

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = "Nostradamus Update For " + db_name
    msg.attach(MIMEText(email_message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()
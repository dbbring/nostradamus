# Nostradamus

## This whole system was designed to up and running ASAP and only to be ran locally. There are numerous safety procedures NOT implemented here simply for the fact that only the developer is going to be using it. 

Currently just pushing changes to master until we have a working release. 

Alphavantage, and IEX api keys should be stored in the sys enviroment variables:
- IEX_API_KEY
- AV_API_KEY

You will also need to install the geckodriver for selenium and put in the .venv enviroment folder (which you also hopefully set up I currently have my bash script and geckodrivers in the .venv folder)

Install the requirements, and set up a cron job to execute the scripts:
- nostradamus.py
- sectors.py

The sectors script needs a database to save to. Preferably the gainers but the sector is simply a one off table that holds unrelated sector info for all the S and P Sectors.

The config json file contains the settings for nostradamus to run correctly. It is defined as:
- Sectors: a database that holds the information from the sectors model.
- Nostradamus : Array of program settings that are defined as:
- - Database name = The database where the resulting Ticker model is stored.
- - Screener Url = The FINVIZ url to be parsed for the stocks that match the upper and lower bounds.
- - Upper Bound = The highest percentage change you are looking for. Use the stock screener URL to define whether you are looking for gainers or losers. We cant turn a negative string into a number so we ditch the minus sign.
- - Lower Bound = The lowest percentage change you are looking for. Use the stock screener URL to define whether you are looking for gainers or losers. We cant turn a negative string into a number so we ditch the minus sign.
- - Stock limit = Number of total tickers you want to process. Useful for rate limiting.
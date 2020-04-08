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


The nostradmaus scripts takes 3 command line parameters:
- Database name
- Upper % limit of stocks your looking to find
- Lower % limit of stocks your looking to find

The reason we using these parameters is so we can have one database with all the gainers and one database with all the losers. However each database is populated exactly the same.

The sector script takes 1 command line paramter:
- Database name

The sectors script needs a database to save to. Preferably the gainers but the sector is simply a one off table that holds unrelated sector info for all the S and P Sectors.
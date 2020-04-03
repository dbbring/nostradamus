# Models
With the exception of the Ticker Model, all models are mirror images of the database table they represent. The ticker model represents a top level model that holds all the other sub models.

## Ticker Model
The ticker model is the top level model that holds all the sub models. Basically for keep one object that we can pass around and maniplute as needed. This way, if something goes wrong, with have the option to not save everything because we dont want incomplete data.

## Tranasction Model
The transaction model is the basic information on the ticker that is trying to be anaylzed. This table merely holds a ID, name, date and percentage change. 

## Price EOD Model
The Price EOD model represents each trading days activities. We have the standard OHLC plus volume, avg volume and of course the date. All subsqeuent anaylzsis will be done from this data. We only save the last week of information (5 Days) even though we need the last 100 days of trading data for our calculations. This model correspond with each Transaction Entry.

## Price Weekly Model
The Price Weekly model represents each weeks trading activites. We have the standard OHLC plus volume and avg volume. This model is basically for anaylzing what macro trend the stock is in. This model correspond with each Transaction Entry.

## Fundamental Model
The Fundmental Model includes all the one off information about the stock. Things from balance sheet info, to institutional information is included in this model. This model correspond with each Transaction Entry.

## Technical Model
The Technical Model includes all the daily anaylsis from the TALIB technical library. Things from bolling bands to rsi are included here. These models correspond with each Price_EOD entry.

## Chart Model
The Chart model includes all the daily charting anaylsis from the TALIB charting library. Things from Dojis to Morning Stars are included here. These models correspond with each Price_EOD entry. The values return for each field are as follows

[] -100 Means No
[] 0 Means Unsure
[] 100 Means Yes

## Sector Model
The Sector model is completely segrated from the rest of the models. It merely holds information about each sector in the S and P, and its daily performance. It also contains daily information on the VIX as well as the Dow, and Nasdaq.
# Models
With the exception of the Ticker Model, all models are mirror images of the database table they represent. The ticker model represents a top level model that holds all the other sub models. The model structure must exactly mimic the table and sql insert structure otherwise the insert will be off.

#### Almost every percent field is stored as a percent already, so dont convert with * 100.

## Ticker Model
The ticker model is the top level model that holds all the sub models. Basically for keep one object that we can pass around and maniplute as needed. This way, if something goes wrong, with have the option to not save everything because we dont want incomplete data.

## Tranasction Model
The transaction model is the basic information on the ticker that is trying to be anaylzed. This table merely holds a ID, name, date and percentage change. 

## Main Price Model
The usual OHLC, volume etc information that everything that uses price action will need.

## Peer Performance Model
This model is for tracking compentitions performance over the same time period. The competitng company is defined as a company in the same geographical area and in the same sector as the subject company. The Area and sectors are dervied from the SEC Edgar.

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

## News Event Model
The News event model holds a list of news articles that could be found from Finviz and TD Ameritrade. Although Nostradamus spefically kicks out tickers with a new article within the last 3 days, its helpful to know what previous articles were and how often the company releases news.

## SEC Model
The SEC Model holds all the information we could find the SEC Edgar. Its the only model that has "sub-models" meaning, the SEC model has an array of SEC_Merger models and so on. SEC information is not deemed highly accurate because of the lack of standards when displaying the information. Therefore it is easy to have null because we simply couldnt find the information requested. Take great care especially when dealing with ADR's. Not only are foreign companies not subject to same reporting requirements, but most of the "shadier" companines only file a 6k so we cant populate most of the sub models.

### SEC_Secondary_Offering (Forms S-3, F-3, F-4, F-6)
The SEC Secondary offering model, is a model to reflect how many times a company has diluated and how many shares the have issued. Although we can be fairly certain how many times they have isseud, we cant be certain of MUCH the diluated. Particularly because the ASR (Automatic Shelf Registration) which means the can issue at any point in time. Also because the SEC tables are not consistant so we cant be certain we found the shares issued.

### SEC_Merger (Form 425)
The SEC merger model simply lists the companies that were in contact with our primary company we are researching. This doesnt guarentee the two companies mergered althought it is highly likely. All we gather is the merging companies name and CIK number. It also possible that it is a restructure within a parent corpartion. There are many possiblities here, so double check that the two companies did actually merger before trusting the data.

### SEC_Employee_Stock (Form S-8)
The Employee stock model list how many times the company has issued additional shares for employee compensation. This gives us a idea of how invested the employees are in the company and also how much more diluation there is.

### SEC_Company_Info (Form 8-K)
The company info is a very light represtation of a 8-K. Becuase it would be almost impossible to verify the langauge and tone of the actual verbage, we are simply collecting which sections the news event belongs to. Are they delisting? is a finicial update? These are all under different sections. We are collecting the link as well, so we can examine the actual form later if desired.

from carbon_black.endpoints.base_endpoint import Endpoint
from carbon_black.endpoints import Charting, EOD, Fundamental, News, Peers, SEC, Sectors, Technical, Weekly, Index
from shared.models import Ticker as Ticker_Model
from datetime import datetime

class Ticker(Endpoint):

  def __init__(self) -> None:
    super().__init__()
    self.api_endpoint = None
    return
    
  def get(self, api_endpoint:str, transaction_id:int) -> dict:
    self.api_endpoint = api_endpoint
    results = self.query(api_endpoint, f"SELECT * FROM Transaction WHERE transaction_id = {transaction_id};")
    response = self.make_ticker_model(results)
    return response[0] if len(response) == 1  else response

  def make_ticker_model(self, sql_results: list):
    all_results = []

    for item in sql_results:
      # Maybe we should have thought JSON when creating our models? Oh well, maybe refactor in the future. For now, this is a mirror image of the Ticker Model.
      model = {}   

      _index = Index()
      _fa = Fundamental()
      _sec = SEC()
      _eod = EOD()
      _news = News()
      _peers = Peers()
      _weekly = Weekly()
      _sectors = Sectors()

      bi = _index.get_by_id(self.api_endpoint, item[0])
      fa = _fa.get(self.api_endpoint, item[0])
      sc = _sec.get(self.api_endpoint, item[0])
      ed = _eod.get(self.api_endpoint, item[0], 'True')
      wk = _weekly.get(self.api_endpoint, item[0])
      nw = _news.get(self.api_endpoint, item[0])
      pe = _peers.get(self.api_endpoint, item[0])

      daily_sector = []
      for eod_item in ed:
        sect = _sectors.get(eod_item['date'], fa[0]['sector']) if fa[0]['sector'] else _sectors.get(item[1].strftime('%Y-%m-%d'))
        daily_sector.append(sect)

      model['basic_info'] = bi[0] if len(bi) == 1 else bi
      model['fund_anaylsis'] = fa[0] if len(fa) ==1 else fa
      model['sec'] = sc[0] if len(sc) == 1 else sc
      model['eod'] = ed[0] if len(ed) == 1 else ed
      model['weekly'] = wk[0] if len(wk) == 1 else wk
      model['news'] = nw[0] if len(nw) == 1 else nw
      model['peers'] = pe[0] if len(pe) == 1 else pe
      model['sector_performance'] = daily_sector[0] if len(daily_sector) == 1 else daily_sector
      model['sector_historic_performance'] = _sectors.make_all_sectors_performance(fa[0]['sector']) if fa[0]['sector'] else _sectors.get(item[1].strftime('%Y-%m-%d'))

      all_results.append(model)

    return all_results


from shared.base_model import Base_Model


# ======================================================= #
#                Main Ticker Object                       #
# ======================================================= #

class Ticker(object):

  def __init__(self, symbol):
    return

  basic_info = Transaction()
  intraday = [Price_Detail()]
  eod = [Price_EOD()]
  weekly = [Price_Weekly()]
  tech_anaylsis = [Technical_Indicators()]
  fund_anaylsis = Fundamental_Indicators()
  chart_anaylsis = [Chart_Indicators()]


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ======================================================= #
#                 Sectors Table                           #
# ======================================================= #

# All Values are already percentages! No need to * 100 to get a true percent value. Except for the VIX CLOSE.
# These sectors are based on the S and P sectors.
# make list of sub cats and direct to top level cat
# hit fin model prep for all indicies and calc percent change still need vix and futures

class Sectors(Base_Model):

  def __init__(self):
    return

  default_float = Base_Model.default_float

  insert_sql = ('INSERT INTO Sectors ('
    'date, s_p, dji, nasdaq, russell_1000, russell_2000, vix, vix_close,'
    'real_estate, consumer_staples, health_care, utilities, materials,'
    'industrials, financials, energy,communication_services,'
    'consumer_discretionary, information_technology) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

  data = {
    'sector_id': None,
    'date': None,
    's_p': default_float,
    'dji': default_float,
    'nasdaq': default_float,
    'russell_1000': default_float,
    'russell_2000': default_float,
    'vix': default_float,
    'vix_close': default_float,
    'real_estate': default_float,
    'consumer_staples': default_float,
    'health_care': default_float,
    'utilities': default_float,
    'materials': default_float,
    'industrials': default_float,
    'financials': default_float,
    'energy': default_float,
    'communication_services': default_float,
    'consumer_discretionary': default_float,
    'information_technology': default_float
  }

  def get_sector(self, sector: str) -> str:
    # returns the proper top level data name for a sub
    sanitizeSector = sector.lower()
    sanitizeSector = sanitizeSector.replace(' ', '')
    sanitizeSector = sanitizeSector.replace('-', '')
    sanitizeSector = sanitizeSector.replace('_', '')
    sanitizeSector = sanitizeSector.replace('&', '')

    health_care = set(['healthcareequipmentandservices', 'healthcareequipmentservices', 'pharmaceuticals,biotechnologyandlifesciences', 'pharmaceuticals,biotechnology,lifesciences', 'pharmaceuticals', 'biotechnology', 'pharmaceuticals','lifesciences', 'pharmaceutical', 'healthcare'])
    it = set(['technologyhardwareequipment', 'technology', 'hardware','semiconductorssemiconductorequipment', 'semiconductors','semiconductorequipment','informationtechnology', 'software', 'softwareservices'])
    comm_serv = set(['communicationservices', 'communicationservice','telecommunicationservices', 'mediaentertainment','media', 'entertainment'])
    comm_staples = set(['consumerstaples', 'consumerstaple','foodstaplesretailing', 'food','staples', 'householpersonalproducts', 'household', 'personalproducts', 'foodbeveragetobacco', 'foodbeverage', 'tobacco'])
    comm_disc = set(['consumerdiscretionary', 'automobilescomponents', 'automobiles','consumerservices', 'consumerdurablesapparel', 'apparel', 'consumerdurables', 'retailing'])
    indust = set(['industrials', 'industrial', 'commercialprofessional services','professionalservices', 'transportation', 'capitalgoods'])
    financ = set(['financials', 'financial', 'insurance', 'banks', 'bank', 'banking', 'diversifiedfinancials'])


    if sanitizeSector == 'realestate':
      return 'real_estate'
    elif sanitizeSector == 'utilities':
      return 'utilities'
    elif sanitizeSector == 'materials':
      return 'materials'
    elif sanitizeSector == 'energy':
      return 'energy'
    elif sanitizeSector in health_care:
      return 'health_care'
    elif sanitizeSector in it:
      return 'information_technology'
    elif sanitizeSector in comm_serv:
      return 'communication_services'
    elif sanitizeSector in comm_staples:
      return 'consumer_staples'
    elif sanitizeSector in comm_disc:
      return 'consumer_discretionary'
    elif sanitizeSector in indust:
      return 'industrials'
    elif sanitizeSector in financ:
      return 'financials'

    return sector
 
# ======================================================= #
#                Transaction Table                        #
# ======================================================= #

class Transaction(Base_Model):

  def __init__(self):
    return


  default_float = Base_Model.default_float
  insert_sql = ''

  data = {
    'transaction_id': None,
    'date': None,
    'ticker': None,
    'sector_change': 0,
    'percent_change': default_float
  }


# ======================================================= #
#    Price End of Day - Transaction Bridge Table          #
# ======================================================= #

class PEOD_Transact_Bridge(Base_Model):

  def __init__(self):
      return


  default_float = Base_Model.default_float
  insert_sql = ''

  data = {
    'row_id': None,
    'tranasction_id': None,
    'eod_id': None
  }


# ======================================================= #
#                Price End of Day Table                   #
# ======================================================= #

class Price_EOD(Base_Model):

  def __init__(self):
      return


  default_float = Base_Model.default_float
  default_int = Base_Model.default_int
  insert_sql = ''

  data = {
    'eod_id': None,
    'is_tracking_period': None,
    'date': None,
    'open': default_int,
    'high': default_int,
    'low': default_int,
    'close': default_int,
    'volume': default_float,
    'avg_volume': default_float,
    'percent_change': default_float
  }

    
# ======================================================= #
#    Price Weekly - Transaction Bridge Table          #
# ======================================================= #

class PW_Transact_Bridge(Base_Model):

  def __init__(self):
      return


  default_float = Base_Model.default_float
  insert_sql = ''

  data = {
    'row_id': None,
    'transaction_id': None,
    'pw_id': None
  }


# ======================================================= #
#                Price Weekly Table                       #
# ======================================================= #

class Price_Weekly(Base_Model):

  def __init__(self):
      return


  default_float = Base_Model.default_float
  default_int = Base_Model.default_int
  insert_sql = ''

  data = {
    'weekly_id': None,
    'open': default_int,
    'high': default_int,
    'low': default_int,
    'close': default_int,
    'volume': default_int,
    'avg_volume': default_int,
    'percent_change': default_float,
    'date': None
  }
        

# ======================================================= #
#          Price EOD - Price Detail Bridge Table          #
# ======================================================= #

class PEOD_PD_Bridge(Base_Model):

  def __init__(self):
    return


  default_float = Base_Model.default_float
  default_int = Base_Model.default_int
  insert_sql = ''

  data = {
    'row_id': None,
    'eod_id': None,
    'price_detail_id': None
  }


# ======================================================= #
#                Price per Day (30Min) Table              #
# ======================================================= #

class Price_Detail(Base_Model):
  
  def __init__(self):
    return


  default_float = Base_Model.default_float
  default_int = Base_Model.default_int
  insert_sql = ''

  data = {
    'price_detail_id': None,
    'open': default_float,
    'high': default_float,
    'low': default_float,
    'close': default_float,
    'volume': default_float,
    'percent_change': default_float,
    'date': None,
    'time': '',
  }


# ======================================================= #
#              Technical Indicators Table                 #
# ======================================================= #

class Technical_Indicators(Base_Model):
    
  def __init__(self):
    return


  default_float = Base_Model.default_float
  default_int = Base_Model.default_int
  insert_sql = ''

  data = {
    'eod_id': None,
    'atr': default_float,
    'boll_bands': default_float,
    'sma': default_float,
    'ema': default_float,
    'average_directional_movement': default_float,
    'chaikin_osc': default_float,
    'chaikin_a_d_line': default_float,
    'beta': default_float,
    'balance_of_power': default_float,
    'commodity_channel_index': default_float,
    'chande_momentum_oscillator': default_float,
    'pearsons_coefficient': default_float,
    'double_ema': default_float,
    'directional_movement_index': default_float,
    'kaufman_adaptive_ma': default_float,
    'linear_reg': default_float,
    'linear_reg_angle': default_float,
    'linear_reg_intercept': default_float,
    'linear_reg_slope': default_float,
    'macd_conv_diver': default_float,
    'mesa_adaptive_ma': default_float,
    'money_flow_index': default_float,
    'momentum' : default_float,
    'normalized_atr': default_float,
    'obv': default_float,
    'percent_price_osc': default_float,
    'rsi': default_float,
    'parabolic_sar': default_float,
    'parabolic_sar_ext': default_float,
    'std_deviation': default_float,
    'stochastic': default_float,
    'stochastic_fast': default_float,
    'stochastic_rsi': default_float,
    'triple_ema': default_float,
    'true_range': default_float,
    'triangluar_ma': default_float,
    'ultimate_osc': default_float,
    'williams_percent_r': default_float,
    'weighted_ma': default_float,
    'resistance_point': default_float,
    'support_point': default_float,
  }


# ======================================================= #
#             Fundmental Statistics Table                 #
# ======================================================= #

class Fundamental_Indicators(Base_Model):
      
  def __init__(self):
    return


  default_float = Base_Model.default_float
  default_int = Base_Model.default_int
  insert_sql = ''

  data = {
    'transaction_id': None,
    # date of quarter when this data is taken
    'fundemental_date': None,
    # profile
    'beta': default_float,
    'company_name': '',
    # income statement
    'revenue': default_float,
    'revenue_growth': default_float,
    'gross_profit': default_float,
    'eps': default_float,
    'eps_diluted': default_float,
    'divided_per_share': default_float,
    'ebitda_margin': default_float,
    'profit_margin': default_float,
    'ebitda': default_float,
    'net_profit_margin': default_float,
    'free_cash_flow_margin': default_float,
    # Balance sheet
    'cash_and_equivalents': default_float,
    'short_term_debt': default_float,
    'total_current_liabilites': default_float,
    'total_debt': default_float,
    'total_shareholder_equity': default_float,
    'tax_assets': default_float,
    # cash-flow
    'stock_based_compensation': default_float,
    'operating_cash_flow': default_float,
    'capital_expenditure' : default_float,
    'free_cash_flow': default_float,
    # finicial ratios
    'price_book_value_ratio' : default_float,
    'price_to_book_ratio' : default_float,
    'price_to_sales_ratio': default_float,
    'price_earnings_ratio' : default_float,
    'price_to_free_cash_flow_ratio': default_float,
    'price_to_cash_flow_ratio': default_float,
    'earnings_to_growth': default_float,
    'price_sales_ratio': default_float,
    'price_fair_value': default_float,
    'gross_profit_margin': default_float,
    'return_on_assets': default_float,
    'liquidity_current_ratio': default_float,
    'debt_ratio': default_float,
    'debt_equity_ratio': default_float,
    'operating_cash_flows_per_share': default_float,
    'free_cash_flow_per_share': default_float,
    # enterprise value
    'shares_outstanding': default_float,
    'market_cap': default_float,
    'enterprise_value': default_float,
    'revenue_per_share': default_float,
    'cash_per_share': default_float,
    'book_value_per_share': default_float,
    'intrest_debt_per_share': default_float,
    'pe_ratio': default_float,
    'ebitda_enterprise_value': default_float,
    'debt_to_equity': default_float,
    'graham_number': default_float,
    'graham_net_net': default_float,
    'working_capital': default_float,
    'capex_per_share': default_float,
    # growth
    'gross_profit_growth': default_float,
    'operating_income_growth': default_float,
    'net_income_growth': default_float,
    'eps_growth': default_float,
    # dcf
    'discounted_cash_flow': default_float,
    # Other One off data points
    'sector': ''
  }


# ======================================================= #
#                Charting Table                           #
# ======================================================= #

# returns float to say -100 is bearish 100 is bullish

class Chart_Indicators(Base_Model):
        
  def __init__(self):
    return


  default_float = Base_Model.default_float
  default_int = Base_Model.default_int
  insert_sql = ''

  data = {
    'eod_id': None,
    'two_crows': default_float,
    'three_black_crows': default_float,
    'three_inside_up_down': default_float,
    'three_outside_up_down': default_float,
    'three_line_strike': default_float,
    'three_stars_south': default_float,
    'three_adv_soliders': default_float,
    'abandoned_baby': default_float,
    'advance_block': default_float,
    'belt_hold': default_float,
    'breakaway': default_float,
    'marubozu_closing': default_float,
    'concealing_baby_swallow': default_float,
    'counterattack': default_float,
    'dark_cloud_cover': default_float,
    'doji': default_float,
    'doji_star': default_float,
    'doji_dragonfly': default_float,
    'engulfing_pattern': default_float,
    'gravestone_doji': default_float,
    'hammer': default_float,
    'hanging_man': default_float,
    'harami_pattern': default_float,
    'harami_cross_pattern': default_float,
    'high_wave_candle': default_float,
    'hikkake_pattern': default_float,
    'hikkake_mod_pattern': default_float,
    'homing_pigeon': default_float,
    'identical_three_crows': default_float,
    'in_neck_pattern': default_float,
    'inverted_hammer': default_float,
    'kicking': default_float,
    'ladder_bottom': default_float,
    'doji_long_leg': default_float,
    'long_line_candle': default_float,
    'marubozu': default_float,
    'matching_low': default_float,
    'mat_hold': default_float,
    'doji_morning_star': default_float,
    'morning_star': default_float,
    'on_neck_pattern': default_float,
    'piercing_pattern': default_float,
    'rickshaw_man': default_float,
    'rise_fall_three_methods': default_float,
    'seperating_lines': default_float,
    'shooting_star': default_float,
    'short_line_candle': default_float,
    'spinning_top': default_float,
    'stalled_pattern': default_float,
    'stick_sandwhich': default_float,
    'doji_tasuki': default_float,
    'tasuki_gap': default_float,
    'thrusting_pattern': default_float,
    'tristar_pattern': default_float,
    'three_unique_river': default_float,
    'three_upside_gap_river': default_float  
  }
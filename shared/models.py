from shared.base_model import Base_Model
# Populate models?
# or just models of each database????

#  T = Transaction()
# all_variables = vars(T)


# ======================================================= #
#                Main Ticker Object                       #
# ======================================================= #

class Ticker(object):

  def __init__(self):
    return



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ======================================================= #
#                 Sectors Table                           #
# ======================================================= #

# All Values are already percentages! No need to * 100 to get a true percent value.
# These sectors are based on the S and P sectors.

class Sectors(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.schema = {
      'sector_id': None,
      'date': None,
      's_p': 999999.99,
      'real_estate': 999999.99,
      'consumer_staples': 999999.99,
      'health_care': 999999.99,
      'utilities': 999999.99,
      'materials': 999999.99,
      'industrials': 999999.99,
      'financials': 999999.99,
      'energy': 999999.99,
      'communication_services': 999999.99,
      'consumer_discretionary': 999999.99,
      'information_technology': 999999.99
    }
    self.insert_sql = ('INSERT INTO Sectors (' + 
      'date, s_p, real_estate, consumer_staples, health_care,' +
      'utilities, materials, industrials, financials, energy,' +
      'communication_services, consumer_discretionary,information_technology) ' +
     ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    return
 
# ======================================================= #
#                Transaction Table                        #
# ======================================================= #

class Transaction(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.transaction_id = None
    self.date = None
    self.ticker = ''
    self.sector_change = 0
    self.percent_change = 999999.99
    return



# ======================================================= #
#    Price End of Day - Transaction Bridge Table          #
# ======================================================= #

class PEOD_Transact_Bridge(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.row_id = None
    self.transaction_id = None
    self.eod_id = None
    return

# ======================================================= #
#                Price End of Day Table                   #
# ======================================================= #

class Price_EOD(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.eod_id = None
    self.is_tracking_period = True
    self.open = -1
    self.high = -1
    self.low = -1
    self.close = -1
    self.volume = -1
    self.avg_volume = -1
    self.percent_change = 999999.99
    self.date = None
    return
    

# ======================================================= #
#    Price Weekly - Transaction Bridge Table          #
# ======================================================= #

class PW_Transact_Bridge(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.row_id = None
    self.transaction_id = None
    self.pw_id = None
    return


# ======================================================= #
#                Price Weekly Table                       #
# ======================================================= #

class Price_Weekly(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.weekly_id = None
    self.open = -1
    self.high = -1
    self.low = -1
    self.close = -1
    self.volume = -1
    self.avg_volume = -1
    self.percent_change = 999999.99
    self.date = None
    return
        

# ======================================================= #
#          Price EOD - Price Detail Bridge Table          #
# ======================================================= #

class PEOD_PD_Bridge(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.row_id = None
    self.eod_id = None
    self.price_detail_id = None
    return


# ======================================================= #
#                Price per Day (30Min) Table              #
# ======================================================= #

class Price_Detail(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.price_detail_id = None
    self.open = -1
    self.high = -1
    self.low = -1
    self.close = -1
    self.volume = -1
    self.percent_change = 999999.99
    self.date = None
    self.time = ''
    return


# ======================================================= #
#              Technical Indicators Table                 #
# ======================================================= #

class Technical_Indicators(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.eod_id = None
    self.atr = 999999.99
    self.boll_bands = 999999.99
    self.sma = 999999.99
    self.ema = 999999.99
    self.average_directional_movement = 999999.99
    self.chaikin_osc = 999999.99
    self.chaikin_a_d_line = 999999.99
    self.beta = 999999.99
    self.balance_of_power = 999999.99
    self.commodity_channel_index = 999999.99
    self.chande_momentum_oscillator = 999999.99
    self.pearsons_coefficient = 999999.99
    self.double_ema = 999999.99
    self.directional_movement_index = 999999.99
    self.kaufman_adaptive_ma = 999999.99
    self.linear_reg = 999999.99
    self.linear_reg_angle = 999999.99
    self.linear_reg_intercept = 999999.99
    self.linear_reg_slope = 999999.99
    self.macd_conv_diver = 999999.99
    self.mesa_adaptive_ma = 999999.99
    self.money_flow_index = 999999.99
    self.momentum  = 999999.99
    self.normalized_atr = 999999.99
    self.obv = 999999.99
    self.percent_price_osc = 999999.99
    self.rsi = 999999.99
    self.parabolic_sar = 999999.99
    self.parabolic_sar_ext = 999999.99
    self.std_deviation = 999999.99
    self.stochastic = 999999.99
    self.stochastic_fast = 999999.99
    self.stochastic_rsi = 999999.99
    self.triple_ema = 999999.99
    self.true_range = 999999.99
    self.triangluar_ma = 999999.99
    self.ultimate_osc = 999999.99
    self.williams_percent_r = 999999.99
    self.weighted_ma = 999999.99
    self.resistance_point = 999999.99
    self.support_point = 999999.99
    return


# ======================================================= #
#             Fundmental Statistics Table                 #
# ======================================================= #

class Fundamental_Indicators(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.transaction_id = None
    # date of quarter when this data is taken
    self.fundemental_date = None
    # profile
    self.beta = 999999.99
    self.company_name = ''
    # income statement
    self.revenue = 999999.99
    self.revenue_growth = 999999.99
    self.gross_profit = 999999.99
    self.eps = 999999.99
    self.eps_diluted = 999999.99
    self.divided_per_share = 999999.99
    self.ebitda_margin = 999999.99
    self.profit_margin = 999999.99
    self.ebitda = 999999.99
    self.net_profit_margin = 999999.99
    self.free_cash_flow_margin = 999999.99
    # Balance sheet
    self.cash_and_equivalents = 999999.99
    self.short_term_debt = 999999.99
    self.total_current_liabilites = 999999.99
    self.total_debt = 999999.99
    self.total_shareholder_equity = 999999.99
    self.tax_assets = 999999.99
    # cash-flow
    self.stock_based_compensationg = 999999.99
    self.operating_cash_flow = 999999.99
    self.capital_expenditure  = 999999.99
    self.free_cash_flow = 999999.99
    # finicial ratios
    self.price_book_value_ratio  = 999999.99
    self.price_to_book_ratio  = 999999.99
    self.price_to_sales_ratio = 999999.99
    self.price_earnings_ratio  = 999999.99
    self.price_to_free_cash_flow_ratio = 999999.99
    self.price_to_cash_flow_ratio = 999999.99
    self.earnings_to_growth = 999999.99
    self.price_sales_ratio = 999999.99
    self.price_fair_value = 999999.99
    self.gross_profit_margin = 999999.99
    self.return_on_assets = 999999.99
    self.liquidity_current_ratio = 999999.99
    self.debt_ratio = 999999.99
    self.debt_equity_ratio = 999999.99
    self.operating_cash_flows_per_share = 999999.99
    self.free_cash_flow_per_share = 999999.99
    # enterprise value
    self.shares_outstanding = 999999.99
    self.market_cap = 999999.99
    self.enterprise_value = 999999.99
    self.revenue_per_share = 999999.99
    self.cash_per_share = 999999.99
    self.book_value_per_share = 999999.99
    self.intrest_debt_per_share = 999999.99
    self.pe_ratio = 999999.99
    self.ebitda_enterprise_value = 999999.99
    self.debt_to_equity = 999999.99
    self.graham_number = 999999.99
    self.graham_net_net = 999999.99
    self.working_capital = 999999.99
    self.capex_per_share = 999999.99
    # growth
    self.gross_profit_growth = 999999.99
    self.operating_income_growth = 999999.99
    self.net_income_growth = 999999.99
    self.eps_growth = 999999.99
    # dcf
    self.discounted_cash_flow = 999999.99
    return


# ======================================================= #
#                Charting Table                           #
# ======================================================= #

# returns float to say -100 is bearish 100 is bullish

class Chart_Indicators(Base_Model):

  def __init__(self):
    Base_Model.__init__(self)
    self.eod_id = None
    self.two_crows = 999999.99
    self.three_black_crows = 999999.99
    self.three_inside_up_down = 999999.99
    self.three_outside_up_down = 999999.99
    self.three_line_strike = 999999.99
    self.three_stars_south = 999999.99
    self.three_adv_soliders = 999999.99
    self.abandoned_baby = 999999.99
    self.advance_block = 999999.99
    self.belt_hold = 999999.99
    self.breakaway = 999999.99
    self.marubozu_closing = 999999.99
    self.concealing_baby_swallow = 999999.99
    self.counterattack = 999999.99
    self.dark_cloud_cover = 999999.99
    self.doji = 999999.99
    self.doji_star = 999999.99
    self.doji_dragonfly = 999999.99
    self.engulfing_pattern = 999999.99
    self.gravestone_doji = 999999.99
    self.hammer = 999999.99
    self.hanging_man = 999999.99
    self.harami_pattern = 999999.99
    self.harami_cross_pattern = 999999.99
    self.high_wave_candle = 999999.99
    self.hikkake_pattern = 999999.99
    self.hikkake_mod_pattern = 999999.99
    self.homing_pigeon = 999999.99
    self.identical_three_crows = 999999.99
    self.in_neck_pattern = 999999.99
    self.inverted_hammer = 999999.99
    self.kicking = 999999.99
    self.ladder_bottom = 999999.99
    self.doji_long_leg = 999999.99
    self.long_line_candle = 999999.99
    self.marubozu = 999999.99
    self.matching_low = 999999.99
    self.mat_hold = 999999.99
    self.doji_morning_star = 999999.99
    self.morning_star = 999999.99
    self.on_neck_pattern = 999999.99
    self.piercing_pattern = 999999.99
    self.rickshaw_man = 999999.99
    self.rise_fall_three_methods = 999999.99
    self.seperating_lines = 999999.99
    self.shooting_star = 999999.99
    self.short_line_candle = 999999.99
    self.spinning_top = 999999.99
    self.stalled_pattern = 999999.99
    self.stick_sandwhich = 999999.99
    self.doji_tasuki = 999999.99
    self.tasuki_gap = 999999.99
    self.thrusting_pattern = 999999.99
    self.tristar_pattern = 999999.99
    self.three_unique_river = 999999.99
    self.three_upside_gap_river = 999999.99
    return

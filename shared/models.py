from collections import OrderedDict

from shared.base_model import Base_Model

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
  data = OrderedDict()

  data['sector_id'] = None
  data['date'] = None
  data['s_p'] = default_float
  data['dji'] = default_float
  data['nasdaq'] = default_float
  data['russell_1000'] = default_float
  data['russell_2000'] = default_float
  data['vix'] = default_float
  data['vix_close'] = default_float
  data['real_estate'] = default_float
  data['consumer_staples'] = default_float
  data['health_care'] = default_float
  data['utilities'] = default_float
  data['materials'] = default_float
  data['industrials'] = default_float
  data['financials'] = default_float
  data['energy'] = default_float
  data['communication_services'] = default_float
  data['consumer_discretionary'] = default_float
  data['information_technology'] = default_float

  # Class Level Function Just call it and get back what you want
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
  data = OrderedDict()

  data['transaction_id'] = None
  data['date'] = None
  data['ticker'] = None
  data['percent_change'] = default_float


# ======================================================= #
#                Price End of Day Table                   #
# ======================================================= #

class Price_EOD(Base_Model):

  def __init__(self):
      return


  default_float = Base_Model.default_float
  data = OrderedDict()

  data['eod_id'] = None
  data['date'] = None
  data['transaction_id'] = None
  data['is_tracking_period'] = None
  data['open'] = default_float
  data['high'] = default_float
  data['low'] = default_float
  data['close'] = default_float
  data['volume'] = default_float
  data['avg_volume'] = default_float
  data['percent_change'] = default_float


# ======================================================= #
#                Price Weekly Table                       #
# ======================================================= #

class Price_Weekly(Base_Model):

  def __init__(self):
      return


  default_float = Base_Model.default_float
  data = OrderedDict()

  data['weekly_id'] = None
  data['transaction_id'] = None
  data['wk_start_date'] = None
  data['wk_end_date'] = None
  data['open'] = default_float
  data['high'] = default_float
  data['low'] = default_float
  data['close'] = default_float
  data['volume'] = default_float
  data['avg_volume'] = default_float
  data['percent_change'] = default_float


# ======================================================= #
#              Technical Indicators Table                 #
# ======================================================= #

class Technical_Indicators(Base_Model):
    
  def __init__(self):
    return


  default_float = Base_Model.default_float
  data = OrderedDict()

  data['eod_id'] = None
  data['atr'] = default_float
  data['boll_bands'] = default_float
  data['sma'] = default_float
  data['ema'] = default_float
  data['average_directional_movement'] = default_float
  data['chaikin_osc'] = default_float
  data['chaikin_a_d_line'] = default_float
  data['balance_of_power'] = default_float
  data['commodity_channel_index'] = default_float
  data['chande_momentum_oscillator'] = default_float
  data['pearsons_coefficient'] = default_float
  data['double_ema'] = default_float
  data['directional_movement_index'] = default_float
  data['kaufman_adaptive_ma'] = default_float
  data['linear_reg'] = default_float
  data['linear_reg_angle'] = default_float
  data['linear_reg_intercept'] = default_float
  data['linear_reg_slope'] = default_float
  data['macd_conv_diver'] = default_float
  data['mesa_adaptive_ma'] = default_float
  data['money_flow_index'] = default_float
  data['momentum' ] = default_float
  data['normalized_atr'] = default_float
  data['obv'] = default_float
  data['percent_price_osc'] = default_float
  data['rsi'] = default_float
  data['parabolic_sar'] = default_float
  data['parabolic_sar_ext'] = default_float
  data['std_deviation'] = default_float
  data['stochastic'] = default_float
  data['stochastic_fast'] = default_float
  data['stochastic_rsi'] = default_float
  data['triple_ema'] = default_float
  data['true_range'] = default_float
  data['triangluar_ma'] = default_float
  data['ultimate_osc'] = default_float
  data['williams_percent_r'] = default_float
  data['weighted_ma'] = default_float
  data['resistance_point'] = default_float
  data['support_point'] = default_float


# ======================================================= #
#             Fundmental Statistics Table                 #
# ======================================================= #

class Fundamental_Indicators(Base_Model):

  # income statement
  # Finicancals as reported or cash flow or both?
  # Advanced stats
  # Other one off pieces off info
  # next earnings date? dont exclude if they are coming up
  # maybe earnings data
      
  def __init__(self):
    return


  default_float = Base_Model.default_float
  data = OrderedDict()

  data['transaction_id'] = None
  # Income Endpoint
  data['total_revenue'] = default_float
  data['cost_of_revenue'] = default_float
  data['gross_profit'] = default_float
  data['r_and_d'] = default_float
  data['selling_gen_and_admin'] = default_float
  data['operating_expense'] = default_float
  data['operating_income'] = default_float
  data['other_income_expense_net'] = default_float
  data['ebit'] = default_float
  data['intrest_income'] = default_float
  data['pretax_income'] = default_float
  data['income_tax'] = default_float
  data['minority_intrest'] = default_float
  data['net_income'] = default_float
  data['net_income_basic'] = default_float
  # Advanced Stats Endpoint
  data['company_name'] = ''
  data['yr_high'] = default_float
  data['yr_low'] = default_float
  data['yr_change'] = default_float
  data['shares_outstanding'] = default_float
  data['float'] = default_float
  data['eps_ttm'] = default_float
  data['dividend_yield'] = default_float
  data['dividend_rate_ttm'] = default_float
  data['employees'] = default_float
  data['earnings_date'] = None
  data['pe_ratio'] = default_float
  data['beta'] = default_float
  data['total_cash'] = default_float
  data['current_debt'] = default_float
  data['ebitda'] = default_float
  data['revenue_per_share'] = default_float
  data['revenue_per_employee'] = default_float
  data['debt_to_equity'] = default_float
  data['profit_margin'] = default_float
  data['enterprise_value'] = default_float
  data['enterprise_value_to_rev'] = default_float
  data['price_to_sales'] = default_float
  data['price_to_book'] = default_float
  data['foward_pe_ratio'] = default_float
  data['peg_ratio'] = default_float
  data['pe_high'] = default_float
  data['pe_low'] = default_float
  # Cash Flow Endpoint
  data['depreciation'] = default_float
  data['changes_in_receviables'] = default_float
  data['changes_in_inventories'] = default_float
  data['cash_change'] = default_float
  data['cash_flow'] = default_float
  data['capital_expenditures'] = default_float
  data['investments'] = default_float
  data['total_investing_cash_flows'] = default_float
  data['dividends_paid'] = default_float
  data['net_borrowings'] = default_float
  data['other_cash_flows'] = default_float
  data['cash_flow_financing'] = default_float
  # Balance Sheet endpoint
  data['balance_sheet_date'] = None
  data['current_cash'] = default_float
  data['short_term_investments'] = default_float
  data['receivables'] = default_float
  data['inventory'] = default_float
  data['other_current_assets'] = default_float
  data['current_assets'] = default_float
  data['long_term_investments'] = default_float
  data['property_plant_equipment'] = default_float
  data['goodwill'] = default_float
  data['intangible_assets'] = default_float
  data['other_assets'] = default_float
  data['total_assets'] = default_float
  data['accounts_payable'] = default_float
  data['current_long_term_debt'] = default_float
  data['other_current_liabilites'] = default_float
  data['total_current_liabilites'] = default_float
  data['long_term_debt'] = default_float
  data['other_liabilites'] = default_float
  data['minority_interest'] = default_float
  data['total_liabilites'] = default_float
  data['common_stock'] = default_float
  data['retained_earnings'] = default_float
  data['treasury_stock'] = default_float
  data['capital_surplus'] = default_float
  data['shareholder_equity'] = default_float
  data['net_tangible_assets'] = default_float
  # Financial Ratios Calc'd on the fly no endpoint
  # https://www.oldschoolvalue.com/financials-accounting/balance-sheet-ratios/
  data['quick_ratio'] = default_float
  data['current_ratio'] = default_float
  data['total_debt_equity_ratio'] = default_float
  data['long_term_debt_equity'] = default_float
  data['short_term_debt_equity'] = default_float
  data['avg_age_of_inventory'] = default_float
  data['intangibles_book_ratio'] = default_float
  data['inventory_to_sales_ratio'] = default_float
  data['long_term_debt_percent_invest_cap'] = default_float
  data['short_term_debt_percent_invest_cap'] = default_float
  data['long_term_debt_to_total_debt'] = default_float
  data['short_term_debt_to_total_debt'] = default_float
  data['total_liabilites_to_total_assets'] = default_float
  data['working_capital'] = default_float
  # Other One off data points with advanced stats
  data['sector'] = ''
  data['sector_change'] = default_float
  data['avg_30_volume'] = default_float
  data['mvg_avg_200'] = default_float
  data['mvg_avg_50'] = default_float
  data['max_change_percent'] = default_float
  data['year_5_change_percent'] = default_float
  data['year_2_change_percent'] = default_float
  data['year_1_change_percent'] = default_float
  data['ytd_change_percent'] = default_float
  data['month_6_change_percent'] = default_float
  data['month_3_change_percent'] = default_float
  data['month_1_change_percent'] = default_float
  data['day_30_change_percent'] = default_float
  data['day_5_change_percent'] = default_float


# ======================================================= #
#                Charting Table                           #
# ======================================================= #

# returns float to say -100 is bearish 100 is bullish

class Chart_Indicators(Base_Model):
        
  def __init__(self):
    return


  default_float = Base_Model.default_float
  data = OrderedDict()

  data['eod_id'] = None
  data['two_crows'] = default_float
  data['three_black_crows'] = default_float
  data['three_inside_up_down'] = default_float
  data['three_outside_up_down'] = default_float
  data['three_line_strike'] = default_float
  data['three_stars_south'] = default_float
  data['three_adv_soliders'] = default_float
  data['abandoned_baby'] = default_float
  data['advance_block'] = default_float
  data['belt_hold'] = default_float
  data['breakaway'] = default_float
  data['marubozu_closing'] = default_float
  data['concealing_baby_swallow'] = default_float
  data['counterattack'] = default_float
  data['dark_cloud_cover'] = default_float
  data['doji'] = default_float
  data['doji_star'] = default_float
  data['doji_dragonfly'] = default_float
  data['engulfing_pattern'] = default_float
  data['gravestone_doji'] = default_float
  data['hammer'] = default_float
  data['hanging_man'] = default_float
  data['harami_pattern'] = default_float
  data['harami_cross_pattern'] = default_float
  data['high_wave_candle'] = default_float
  data['hikkake_pattern'] = default_float
  data['hikkake_mod_pattern'] = default_float
  data['homing_pigeon'] = default_float
  data['identical_three_crows'] = default_float
  data['in_neck_pattern'] = default_float
  data['inverted_hammer'] = default_float
  data['kicking'] = default_float
  data['ladder_bottom'] = default_float
  data['doji_long_leg'] = default_float
  data['long_line_candle'] = default_float
  data['marubozu'] = default_float
  data['matching_low'] = default_float
  data['mat_hold'] = default_float
  data['doji_morning_star'] = default_float
  data['morning_star'] = default_float
  data['on_neck_pattern'] = default_float
  data['piercing_pattern'] = default_float
  data['rickshaw_man'] = default_float
  data['rise_fall_three_methods'] = default_float
  data['seperating_lines'] = default_float
  data['shooting_star'] = default_float
  data['short_line_candle'] = default_float
  data['spinning_top'] = default_float
  data['stalled_pattern'] = default_float
  data['stick_sandwhich'] = default_float
  data['doji_tasuki'] = default_float
  data['tasuki_gap'] = default_float
  data['thrusting_pattern'] = default_float
  data['tristar_pattern'] = default_float
  data['three_unique_river'] = default_float
  data['three_upside_gap_river'] = default_float  

# ======================================================= #
#                Main Ticker Object                       #
# ======================================================= #

class Ticker(object):

  def __init__(self):
    return

  basic_info = Transaction()
  eod = [Price_EOD()]
  weekly = [Price_Weekly()]
  tech_anaylsis = [Technical_Indicators()]
  fund_anaylsis = Fundamental_Indicators()
  chart_anaylsis = [Chart_Indicators()]
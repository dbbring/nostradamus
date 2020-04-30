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
    self.default_float = Base_Model.default_float
    self.data = OrderedDict()

    self.data['sector_id'] = None
    self.data['date'] = None
    self.data['s_p'] = self.default_float
    self.data['dji'] = self.default_float
    self.data['nasdaq'] = self.default_float
    self.data['russell_1000'] = self.default_float
    self.data['russell_2000'] = self.default_float
    self.data['vix'] = self.default_float
    self.data['vix_close'] = self.default_float
    self.data['real_estate'] = self.default_float
    self.data['consumer_staples'] = self.default_float
    self.data['health_care'] = self.default_float
    self.data['utilities'] = self.default_float
    self.data['materials'] = self.default_float
    self.data['industrials'] = self.default_float
    self.data['financials'] = self.default_float
    self.data['energy'] = self.default_float
    self.data['communication_services'] = self.default_float
    self.data['consumer_discretionary'] = self.default_float
    self.data['information_technology'] = self.default_float
    return

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
    self.default_float = Base_Model.default_float
    self.data = OrderedDict()

    self.data['transaction_id'] = None
    self.data['date'] = None
    self.data['ticker'] = None
    self.data['percent_change'] = self.default_float
    return


# ======================================================= #
#                Main Price Model                         #
# ======================================================= #

class Price(Base_Model):

  def __init__(self):
    self.default_float = Base_Model.default_float
    self.data = OrderedDict()

    self.data['eod_id'] = None
    self.data['transaction_id'] = None
    self.data['date'] = None
    self.data['open'] = self.default_float
    self.data['high'] = self.default_float
    self.data['low'] = self.default_float
    self.data['close'] = self.default_float
    self.data['volume'] = self.default_float
    self.data['percent_change'] = self.default_float
    return


# ======================================================= #
#                Price End of Day Table                   #
# ======================================================= #

class Price_EOD(Price):

  def __init__(self):
    self.default_float = Base_Model.default_float
    self.data = Price().data

    
    self.data['is_tracking_period'] = None
    self.data['avg_volume'] = self.default_float #50 day period
    return


# ======================================================= #
#                Price Weekly Table                       #
# ======================================================= #

class Price_Weekly(Base_Model):

  def __init__(self):
    self.default_float = Base_Model.default_float
    self.data = OrderedDict()

    self.data['weekly_id'] = None
    self.data['transaction_id'] = None
    self.data['date'] = None
    self.data['open'] = self.default_float
    self.data['high'] = self.default_float
    self.data['low'] = self.default_float
    self.data['close'] = self.default_float
    self.data['volume'] = self.default_float
    self.data['avg_volume'] = self.default_float
    self.data['percent_change'] = self.default_float
    return


# ======================================================= #
#    Competitions Price Performance in the same Sector    #
# ======================================================= #

class Peer_Performance(Price):

  def __init__(self):
    self.default_float = Base_Model.default_float
    self.data = Price().data

    self.data['ticker'] = None
    return


# ======================================================= #
#                 News Event Table                        #
# ======================================================= #

class News_Event(Base_Model):

  def __init__(self):
    self.data = OrderedDict()

    self.data['news_event_id'] = None
    self.data['transaction_id'] = None
    self.data['date_of_article'] = None
    self.data['title_of_article'] = None
    self.data['link'] = None
    self.data['source'] = None
    return


# ======================================================= #
#              Technical Indicators Table                 #
# ======================================================= #

class Technical_Indicators(Base_Model):
    
  def __init__(self):
    self.default_float = Base_Model.default_float
    self.data = OrderedDict()

    self.data['eod_id'] = None
    self.data['atr_3_period'] = self.default_float # Measures volatility
    self.data['atr_10_period'] = self.default_float
    self.data['atr_15_period'] = self.default_float
    self.data['atr_20_period'] = self.default_float
    self.data['boll_bands_upper_3_period'] = self.default_float
    self.data['boll_bands_middle_3_period'] = self.default_float
    self.data['boll_bands_lower_3_period'] = self.default_float
    self.data['boll_bands_upper_10_period'] = self.default_float
    self.data['boll_bands_middle_10_period'] = self.default_float
    self.data['boll_bands_lower_10_period'] = self.default_float
    self.data['boll_bands_upper_15_period'] = self.default_float
    self.data['boll_bands_middle_15_period'] = self.default_float
    self.data['boll_bands_lower_15_period'] = self.default_float
    self.data['boll_bands_upper_20_period'] = self.default_float
    self.data['boll_bands_middle_20_period'] = self.default_float
    self.data['boll_bands_lower_20_period'] = self.default_float
    self.data['sma_3_period'] = self.default_float
    self.data['sma_10_period'] = self.default_float
    self.data['sma_15_period'] = self.default_float
    self.data['sma_20_period'] = self.default_float
    self.data['ema_3_period'] = self.default_float
    self.data['ema_10_period'] = self.default_float
    self.data['ema_15_period'] = self.default_float
    self.data['ema_20_period'] = self.default_float
    self.data['average_directional_movement_3_period'] = self.default_float
    self.data['average_directional_movement_10_period'] = self.default_float
    self.data['average_directional_movement_15_period'] = self.default_float
    self.data['average_directional_movement_20_period'] = self.default_float
    self.data['chaikin_osc_fast_3_slow_10'] = self.default_float
    self.data['chaikin_osc_fast_6_slow_18'] = self.default_float
    self.data['chaikin_osc_fast_10_slow_20'] = self.default_float
    self.data['chaikin_a_d_line'] = self.default_float
    self.data['balance_of_power'] = self.default_float
    self.data['commodity_channel_index_3_period'] = self.default_float
    self.data['commodity_channel_index_10_period'] = self.default_float
    self.data['commodity_channel_index_15_period'] = self.default_float
    self.data['commodity_channel_index_20_period'] = self.default_float
    self.data['chande_momentum_oscillator_3_period'] = self.default_float
    self.data['chande_momentum_oscillator_10_period'] = self.default_float
    self.data['chande_momentum_oscillator_15_period'] = self.default_float
    self.data['chande_momentum_oscillator_20_period'] = self.default_float
    self.data['pearsons_coeff_close_vol_5_period'] = self.default_float 
    self.data['pearsons_coeff_close_vol_15_period'] = self.default_float
    self.data['pearsons_coeff_close_vol_30_period'] = self.default_float
    self.data['pearsons_coeff_close_avg_vol_5_period'] = self.default_float 
    self.data['pearsons_coeff_close_avg_vol_15_period'] = self.default_float
    self.data['pearsons_coeff_close_avg_vol_30_period'] = self.default_float
    self.data['pearsons_coeff_close_spy_5_period'] = self.default_float 
    self.data['pearsons_coeff_close_spy_15_period'] = self.default_float
    self.data['pearsons_coeff_close_spy_30_period'] = self.default_float
    self.data['double_ema_3_period'] = self.default_float
    self.data['double_ema_10_period'] = self.default_float
    self.data['double_ema_15_period'] = self.default_float
    self.data['double_ema_20_period'] = self.default_float
    self.data['directional_movement_index_3_period'] = self.default_float
    self.data['directional_movement_index_10_period'] = self.default_float
    self.data['directional_movement_index_15_period'] = self.default_float
    self.data['directional_movement_index_20_period'] = self.default_float
    self.data['kaufman_adaptive_ma_5_period'] = self.default_float
    self.data['kaufman_adaptive_ma_15_period'] = self.default_float
    self.data['kaufman_adaptive_ma_30_period'] = self.default_float
    self.data['linear_reg_3_period'] = self.default_float
    self.data['linear_reg_10_period'] = self.default_float
    self.data['linear_reg_15_period'] = self.default_float
    self.data['linear_reg_20_period'] = self.default_float
    self.data['linear_reg_angle_3_period'] = self.default_float
    self.data['linear_reg_angle_10_period'] = self.default_float
    self.data['linear_reg_angle_15_period'] = self.default_float
    self.data['linear_reg_angle_20_period'] = self.default_float
    self.data['linear_reg_intercept_3_period'] = self.default_float
    self.data['linear_reg_intercept_10_period'] = self.default_float
    self.data['linear_reg_intercept_15_period'] = self.default_float
    self.data['linear_reg_intercept_20_period'] = self.default_float
    self.data['linear_reg_slope_3_period'] = self.default_float
    self.data['linear_reg_slope_10_period'] = self.default_float
    self.data['linear_reg_slope_15_period'] = self.default_float
    self.data['linear_reg_slope_20_period'] = self.default_float
    self.data['macd_fast_12_slow_26_sig_9'] = self.default_float
    self.data['macd_signal_fast_12_slow_26_sig_9'] = self.default_float
    self.data['macd_hist_fast_12_slow_26_sig_9'] = self.default_float
    self.data['macd_fast_6_slow_13_sig_5'] = self.default_float
    self.data['macd_signal_fast_6_slow_13_sig_5'] = self.default_float
    self.data['macd_hist_fast_6_slow_13_sig_5'] = self.default_float
    self.data['macd_fast_18_slow_39_sig_14'] = self.default_float
    self.data['macd_signal_fast_18_slow_39_sig_14'] = self.default_float
    self.data['macd_hist_fast_18_slow_39_sig_14'] = self.default_float
    self.data['mesa_adaptive_ma_mama'] = self.default_float
    self.data['mesa_adaptive_ma_fama'] = self.default_float
    self.data['money_flow_index_3_period'] = self.default_float
    self.data['money_flow_index_10_period'] = self.default_float
    self.data['money_flow_index_15_period'] = self.default_float
    self.data['money_flow_index_20_period'] = self.default_float
    self.data['momentum_3_period'] = self.default_float
    self.data['momentum_10_period'] = self.default_float
    self.data['momentum_15_period'] = self.default_float
    self.data['momentum_20_period'] = self.default_float
    self.data['normalized_atr_3_period'] = self.default_float
    self.data['normalized_atr_10_period'] = self.default_float
    self.data['normalized_atr_15_period'] = self.default_float
    self.data['normalized_atr_20_period'] = self.default_float
    self.data['obv'] = self.default_float
    self.data['percent_price_osc_fast_6_slow_13'] = self.default_float
    self.data['percent_price_osc_fast_12_slow_26'] = self.default_float
    self.data['percent_price_osc_fast_18_slow_38'] = self.default_float
    self.data['rsi_3_period'] = self.default_float
    self.data['rsi_10_period'] = self.default_float
    self.data['rsi_15_period'] = self.default_float
    self.data['rsi_20_period'] = self.default_float
    self.data['parabolic_sar'] = self.default_float
    self.data['parabolic_sar_ext'] = self.default_float
    self.data['std_deviation_3_period'] = self.default_float
    self.data['std_deviation_10_period'] = self.default_float
    self.data['std_deviation_15_period'] = self.default_float
    self.data['std_deviation_20_period'] = self.default_float
    self.data['std_deviation_dbl_3_period'] = self.default_float
    self.data['std_deviation_dbl_10_period'] = self.default_float
    self.data['std_deviation_dbl_15_period'] = self.default_float
    self.data['std_deviation_dbl_20_period'] = self.default_float
    self.data['stochastic_sk_fast_5_slow_k_3_slow_d_3'] = self.default_float
    self.data['stochastic_sd_fast_5_slow_k_3_slow_d_3'] = self.default_float
    self.data['stochastic_sk_fast_20_slow_k_7_slow_d_7'] = self.default_float
    self.data['stochastic_sd_fast_20_slow_k_7_slow_d_7'] = self.default_float
    self.data['stochastic_sk_fast_20_slow_k_14_slow_d_14'] = self.default_float
    self.data['stochastic_sd_fast_20_slow_k_14_slow_d_14'] = self.default_float
    self.data['triple_ema_3_period'] = self.default_float
    self.data['triple_ema_10_period'] = self.default_float
    self.data['triple_ema_15_period'] = self.default_float
    self.data['true_range'] = self.default_float
    self.data['triangluar_ma_15_period'] = self.default_float
    self.data['triangluar_ma_30_period'] = self.default_float
    self.data['ultimate_osc_3_6_12_period'] = self.default_float
    self.data['ultimate_osc_7_14_28_period'] = self.default_float
    self.data['ultimate_osc_10_20_40_period'] = self.default_float
    self.data['williams_percent_r_3_period'] = self.default_float
    self.data['williams_percent_r_10_period'] = self.default_float
    self.data['williams_percent_r_15_period'] = self.default_float
    self.data['williams_percent_r_20_period'] = self.default_float
    self.data['weighted_ma_3_period'] = self.default_float
    self.data['weighted_ma_10_period'] = self.default_float
    self.data['weighted_ma_15_period'] = self.default_float
    self.data['weighted_ma_20_period'] = self.default_float
    return


# ======================================================= #
#             Fundmental Statistics Table                 #
# ======================================================= #

class Fundamental_Indicators(Base_Model):
      
  def __init__(self):
    self.default_float = Base_Model.default_float
    self.data = OrderedDict()

    self.data['transaction_id'] = None
    # Income Endpoint
    self.data['total_revenue'] = self.default_float
    self.data['cost_of_revenue'] = self.default_float
    self.data['gross_profit'] = self.default_float
    self.data['r_and_d'] = self.default_float
    self.data['selling_gen_and_admin'] = self.default_float
    self.data['operating_expense'] = self.default_float
    self.data['operating_income'] = self.default_float
    self.data['other_income_expense_net'] = self.default_float
    self.data['ebit'] = self.default_float
    self.data['intrest_income'] = self.default_float
    self.data['pretax_income'] = self.default_float
    self.data['income_tax'] = self.default_float
    self.data['minority_intrest'] = self.default_float
    self.data['net_income'] = self.default_float
    self.data['net_income_basic'] = self.default_float
    # Advanced Stats Endpoint
    self.data['company_name'] = ''
    self.data['yr_high'] = self.default_float
    self.data['yr_low'] = self.default_float
    self.data['yr_change'] = self.default_float
    self.data['shares_outstanding'] = self.default_float
    self.data['float'] = self.default_float
    self.data['eps_ttm'] = self.default_float
    self.data['dividend_yield'] = self.default_float
    self.data['dividend_rate_ttm'] = self.default_float
    self.data['employees'] = self.default_float
    self.data['earnings_date'] = None
    self.data['pe_ratio'] = self.default_float
    self.data['beta'] = self.default_float
    self.data['total_cash'] = self.default_float
    self.data['current_debt'] = self.default_float
    self.data['ebitda'] = self.default_float
    self.data['revenue_per_share'] = self.default_float
    self.data['revenue_per_employee'] = self.default_float
    self.data['debt_to_equity'] = self.default_float
    self.data['profit_margin'] = self.default_float
    self.data['enterprise_value'] = self.default_float
    self.data['enterprise_value_to_rev'] = self.default_float
    self.data['price_to_sales'] = self.default_float
    self.data['price_to_book'] = self.default_float
    self.data['foward_pe_ratio'] = self.default_float
    self.data['peg_ratio'] = self.default_float
    self.data['pe_high'] = self.default_float
    self.data['pe_low'] = self.default_float
    # Cash Flow Endpoint
    self.data['depreciation'] = self.default_float
    self.data['changes_in_receviables'] = self.default_float
    self.data['changes_in_inventories'] = self.default_float
    self.data['cash_change'] = self.default_float
    self.data['cash_flow'] = self.default_float
    self.data['capital_expenditures'] = self.default_float
    self.data['investments'] = self.default_float
    self.data['total_investing_cash_flows'] = self.default_float
    self.data['dividends_paid'] = self.default_float
    self.data['net_borrowings'] = self.default_float
    self.data['other_cash_flows'] = self.default_float
    self.data['cash_flow_financing'] = self.default_float
    # Balance Sheet endpoint
    self.data['balance_sheet_date'] = None
    self.data['current_cash'] = self.default_float
    self.data['short_term_investments'] = self.default_float
    self.data['receivables'] = self.default_float
    self.data['inventory'] = self.default_float
    self.data['other_current_assets'] = self.default_float
    self.data['current_assets'] = self.default_float
    self.data['long_term_investments'] = self.default_float
    self.data['property_plant_equipment'] = self.default_float
    self.data['goodwill'] = self.default_float
    self.data['intangible_assets'] = self.default_float
    self.data['other_assets'] = self.default_float
    self.data['total_assets'] = self.default_float
    self.data['accounts_payable'] = self.default_float
    self.data['current_long_term_debt'] = self.default_float
    self.data['other_current_liabilites'] = self.default_float
    self.data['total_current_liabilites'] = self.default_float
    self.data['long_term_debt'] = self.default_float
    self.data['other_liabilites'] = self.default_float
    self.data['minority_interest'] = self.default_float
    self.data['total_liabilites'] = self.default_float
    self.data['common_stock'] = self.default_float
    self.data['retained_earnings'] = self.default_float
    self.data['treasury_stock'] = self.default_float
    self.data['capital_surplus'] = self.default_float
    self.data['shareholder_equity'] = self.default_float
    self.data['net_tangible_assets'] = self.default_float
    # Financial Ratios Calc'd on the fly no endpoint
    # https://www.oldschoolvalue.com/financials-accounting/balance-sheet-ratios/
    self.data['quick_ratio'] = self.default_float
    self.data['current_ratio'] = self.default_float
    self.data['total_debt_equity_ratio'] = self.default_float
    self.data['long_term_debt_equity'] = self.default_float
    self.data['short_term_debt_equity'] = self.default_float
    self.data['intangibles_book_ratio'] = self.default_float
    self.data['inventory_to_sales_ratio'] = self.default_float
    self.data['long_term_debt_percent_invest_cap'] = self.default_float
    self.data['short_term_debt_percent_invest_cap'] = self.default_float
    self.data['long_term_debt_to_total_debt'] = self.default_float
    self.data['short_term_debt_to_total_debt'] = self.default_float
    self.data['total_liabilites_to_total_assets'] = self.default_float
    self.data['working_capital'] = self.default_float
    # Other One off self.data points with advanced stats
    self.data['sector'] = ''
    self.data['sub_sector'] = ''
    self.data['institutional_ownership'] = self.default_float # already a percent dont convert
    self.data['short_interest_percent'] = self.default_float # already a percent dont convert
    self.data['avg_30_volume'] = self.default_float
    self.data['mvg_avg_200'] = self.default_float
    self.data['mvg_avg_50'] = self.default_float
    self.data['max_change_percent'] = self.default_float
    self.data['year_5_change_percent'] = self.default_float
    self.data['year_2_change_percent'] = self.default_float
    self.data['year_1_change_percent'] = self.default_float
    self.data['ytd_change_percent'] = self.default_float
    self.data['month_6_change_percent'] = self.default_float
    self.data['month_3_change_percent'] = self.default_float
    self.data['month_1_change_percent'] = self.default_float
    self.data['day_30_change_percent'] = self.default_float
    self.data['day_5_change_percent'] = self.default_float
    self.data['resistance_point_avg'] = self.default_float
    self.data['resistance_point'] = self.default_float
    self.data['support_point_avg'] = self.default_float
    self.data['support_point'] = self.default_float
    self.data['book_value'] = self.default_float
    return


# ======================================================= #
#                Charting Table                           #
# ======================================================= #

class Chart_Indicators(Base_Model):
        
  def __init__(self):
    self.default_int = Base_Model.default_int
    self.data = OrderedDict()

    self.data['eod_id'] = None
    self.data['two_crows'] = self.default_int
    self.data['three_black_crows'] = self.default_int
    self.data['three_inside_up_down'] = self.default_int
    self.data['three_outside_up_down'] = self.default_int
    self.data['three_line_strike'] = self.default_int
    self.data['three_stars_south'] = self.default_int
    self.data['three_adv_soliders'] = self.default_int
    self.data['abandoned_baby'] = self.default_int
    self.data['advance_block'] = self.default_int
    self.data['belt_hold'] = self.default_int
    self.data['breakaway'] = self.default_int
    self.data['marubozu_closing'] = self.default_int
    self.data['concealing_baby_swallow'] = self.default_int
    self.data['counterattack'] = self.default_int
    self.data['dark_cloud_cover'] = self.default_int
    self.data['doji'] = self.default_int
    self.data['doji_star'] = self.default_int
    self.data['doji_dragonfly'] = self.default_int
    self.data['engulfing_pattern'] = self.default_int
    self.data['gravestone_doji'] = self.default_int
    self.data['hammer'] = self.default_int
    self.data['hanging_man'] = self.default_int
    self.data['harami_pattern'] = self.default_int
    self.data['harami_cross_pattern'] = self.default_int
    self.data['high_wave_candle'] = self.default_int
    self.data['hikkake_pattern'] = self.default_int
    self.data['hikkake_mod_pattern'] = self.default_int
    self.data['homing_pigeon'] = self.default_int
    self.data['identical_three_crows'] = self.default_int
    self.data['in_neck_pattern'] = self.default_int
    self.data['inverted_hammer'] = self.default_int
    self.data['kicking'] = self.default_int
    self.data['ladder_bottom'] = self.default_int
    self.data['doji_long_leg'] = self.default_int
    self.data['long_line_candle'] = self.default_int
    self.data['marubozu'] = self.default_int
    self.data['matching_low'] = self.default_int
    self.data['mat_hold'] = self.default_int
    self.data['doji_morning_star'] = self.default_int
    self.data['morning_star'] = self.default_int
    self.data['on_neck_pattern'] = self.default_int
    self.data['piercing_pattern'] = self.default_int
    self.data['rickshaw_man'] = self.default_int
    self.data['rise_fall_three_methods'] = self.default_int
    self.data['seperating_lines'] = self.default_int
    self.data['shooting_star'] = self.default_int
    self.data['short_line_candle'] = self.default_int
    self.data['spinning_top'] = self.default_int
    self.data['stalled_pattern'] = self.default_int
    self.data['stick_sandwhich'] = self.default_int
    self.data['doji_tasuki'] = self.default_int
    self.data['tasuki_gap'] = self.default_int
    self.data['thrusting_pattern'] = self.default_int
    self.data['tristar_pattern'] = self.default_int
    self.data['three_unique_river'] = self.default_int
    self.data['three_upside_gap_river'] = self.default_int  
    return


# ======================================================= #
#                SEC Secondary Offering Table (S-3)       #
# ======================================================= #

class SEC_Secondary_Offering(Base_Model):
        
  def __init__(self):
    self.default_int = Base_Model.default_int
    self.data = OrderedDict()

    self.data['sec_secondary_offering_id'] = None
    self.data['sec_id'] = None
    self.data['date'] = None
    self.data['additional_shares_issued'] = self.default_int
    self.data['is_asr'] = None # Automatic Shelf Registration
    self.data['link'] = None

    return


# ======================================================= #
#                       SEC Merger Table (425)            #
# ======================================================= #

class SEC_Merger(Base_Model):
        
  def __init__(self):
    self.default_int = Base_Model.default_int
    self.data = OrderedDict()

    self.data['sec_merger_id'] = None
    self.data['sec_id'] = None
    self.data['date'] = None # very first 425
    self.data['merging_with_company'] = None
    self.data['merging_with_cik'] = None

    return


# ======================================================= #
#            SEC Employee Stock Program Table (S-8)       #
# ======================================================= #

class SEC_Employee_Stock(Base_Model):
        
  def __init__(self):
    self.default_int = Base_Model.default_int
    self.data = OrderedDict()

    self.data['sec_employee_stock_id'] = None
    self.data['sec_id'] = None
    self.data['date'] = None
    self.data['additional_shares_issued'] = self.default_int
    self.data['link'] = None

    return


# ======================================================= #
#            SEC Changes in Information Table (8-K)       #
# ======================================================= #

class SEC_Company_Info(Base_Model):
        
  def __init__(self):
    self.default_int = Base_Model.default_int
    self.data = OrderedDict()

    self.data['sec_company_info_id'] = None
    self.data['sec_id'] = None
    self.data['date'] = None 
    self.data['link'] = None
    self.data['item_list'] = {} # Key (Item Num) Value (Item Descrip)

    return


# ======================================================= #
#                SEC Info Table                           #
# ======================================================= #

class SEC(Base_Model):
        
  def __init__(self):
    self.default_int = Base_Model.default_int
    self.data = OrderedDict()

    self.data['sec_id'] = None
    self.data['transaction_id'] = None
    self.data['date_of_ipo'] = None
    self.data['late_filings'] = self.default_int
    self.data['ct_orders'] = self.default_int
    self.data['is_adr'] = None
    self.data['company_info'] = [] #[SEC_Company_Info(), ..]
    self.data['secondary_offerings'] = [] # [SEC_Secondary_Offering()..]
    self.data['mergers'] = [] # [SEC_Merger(), ..]
    self.data['stock_program'] = [] # [SEC_Employee_Stock, ..]

    return


# ======================================================= #
#                Main Ticker Object                       #
# ======================================================= #

class Ticker(object):

  def __init__(self):

    # DB SAVE USES THE FIELD NAME! MAKE SURE TO ACCOUNT FOR IT!

    self.basic_info = Transaction()
    self.fund_anaylsis = None # Fundamental_Indicators()
    self.sec = None # SEC()
    self.eod = [] # [Price_EOD(), Price_EOD()]
    self.weekly = [] # [Price_Weekly(), Price_Weekly()]
    self.tech_anaylsis = [] # [Technical_Indicators(), Technical_Indicators()]
    self.chart_anaylsis =[] # [Chart_Indicators(), Chart_Indicators()]
    self.news = [] # [News_Event(), News_Event()]
    self.peers = [] # [Peer_Performance(), Peer_Performance()]
    return

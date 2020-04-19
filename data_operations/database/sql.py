#! /usr/bin/env python

# ===============================================================
#           Schema of Nostradamus Database
# ===============================================================

class DB_SCHEMA(object):

  # @params (None)
  # @descrip None
  # @returns None
  def __init__(self):
    return

  # @params (None)
  # @descrip - The insert statements that corresponds to correct model (aka db table). So when the cursor called, it provides the data and the insert statement provides the SQL.
  # @returns None
  def insert_statements(self):
    INSERT_SQL = {}

    INSERT_SQL['Sectors'] = ('INSERT INTO Sectors ('
    'date, s_p, dji, nasdaq, russell_1000, russell_2000, vix, vix_close,'
    'real_estate, consumer_staples, health_care, utilities, materials,'
    'industrials, financials, energy,communication_services,'
    'consumer_discretionary, information_technology) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['Transaction'] = ('INSERT INTO Transaction ('
    'date, ticker, percent_change) VALUES '
    '(%s, %s, %s)')

    INSERT_SQL['Price_EOD'] = ('INSERT INTO Price_EOD ('
    'transaction_id, date, open, high, low, close, volume, percent_change, is_tracking_period, avg_volume) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['Price_Weekly'] = ('INSERT INTO Price_Weekly ('
    'transaction_id, wk_start_date, wk_end_date, open, high, '
    'low, close, volume, avg_volume, percent_change) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['Peer_Performance'] = ('INSERT INTO Peer_Performance (transaction_id, date, open, high, low, close, volume, percent_change, ticker) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['News_Event'] = ('INSERT INTO News_Event ('
    'transaction_id, date_of_article,title_of_article, link, source) VALUES '
    '(%s, %s, %s, %s, %s)')

    INSERT_SQL['SEC'] = ('INSERT INTO SEC ('
    'transaction_id, date_of_ipo, late_filings, ct_orders, is_adr) VALUES '
    '(%s, %s, %s, %s, %s)')

    INSERT_SQL['SEC_Company_Info'] = ('INSERT INTO SEC_Company_Info ('
    'sec_id, date, link, item_list) VALUES '
    '(%s, %s, %s, %s)')

    INSERT_SQL['SEC_Employee_Stock'] = ('INSERT INTO SEC_Employee_Stock ('
    'sec_id, date, additional_shares_issued, link) VALUES '
    '(%s, %s, %s, %s)')

    INSERT_SQL['SEC_Merger'] = ('INSERT INTO SEC_Merger ('
    'sec_id, date, merging_with_company, merging_with_cik) VALUES '
    '(%s, %s, %s, %s)')

    INSERT_SQL['SEC_Secondary_Offering'] = ('INSERT INTO SEC_Secondary_Offering (sec_id, date, additional_shares_issued, is_asr, link) VALUES '
    '(%s, %s, %s, %s, %s)')

    INSERT_SQL['Technical_Indicators'] = ('INSERT INTO Technical_Indicators (eod_id,' 
    'atr_3_period, atr_10_period, atr_15_period, atr_20_period, boll_bands_upper_3_period,'    'boll_bands_middle_3_period, boll_bands_lower_3_period, boll_bands_upper_10_period,' 'boll_bands_middle_10_period, boll_bands_lower_10_period, boll_bands_upper_15_period,'    'boll_bands_middle_15_period, boll_bands_lower_15_period, boll_bands_upper_20_period,' 'boll_bands_middle_20_period, boll_bands_lower_20_period, sma_3_period, sma_10_period,'    'sma_15_period, sma_20_period, ema_3_period, ema_10_period, ema_15_period,'    'ema_20_period, average_directional_movement_3_period,' 'average_directional_movement_10_period, average_directional_movement_15_period,'    'average_directional_movement_20_period, chaikin_osc_fast_3_slow_10, '   'chaikin_osc_fast_6_slow_18, chaikin_osc_fast_10_slow_20, chaikin_a_d_line,'    'balance_of_power, commodity_channel_index_3_period, commodity_channel_index_10_period,'    'commodity_channel_index_15_period, commodity_channel_index_20_period,  '  'chande_momentum_oscillator_3_period, chande_momentum_oscillator_10_period, '   'chande_momentum_oscillator_15_period, chande_momentum_oscillator_20_period, '   'pearsons_coeff_close_vol_5_period, pearsons_coeff_close_vol_15_period,  '  'pearsons_coeff_close_vol_30_period, pearsons_coeff_close_avg_vol_5_period,'
    'pearsons_coeff_close_avg_vol_15_period, pearsons_coeff_close_avg_vol_30_period, '   'pearsons_coeff_close_sp_5_period, pearsons_coeff_close_sp_15_period, '   'pearsons_coeff_close_sp_30_period, double_ema_3_period, double_ema_10_period, '   'double_ema_15_period, double_ema_20_period, directional_movement_index_3_period,'    'directional_movement_index_10_period, directional_movement_index_15_period, '   'directional_movement_index_20_period, kaufman_adaptive_ma_5_period, '   'kaufman_adaptive_ma_15_period, kaufman_adaptive_ma_30_period, linear_reg_3_period,'    'linear_reg_10_period, linear_reg_15_period, linear_reg_20_period,'   'linear_reg_angle_3_period, linear_reg_angle_10_period, linear_reg_angle_15_period,'    'linear_reg_angle_20_period, linear_reg_intercept_3_period, linear_reg_intercept_10_period,' 'linear_reg_intercept_15_period, linear_reg_intercept_20_period, linear_reg_slope_3_period,' 'linear_reg_slope_10_period, linear_reg_slope_15_period, linear_reg_slope_20_period, '   'macd_fast_12_slow_26_sig_9, macd_signal_fast_12_slow_26_sig_9,' 'macd_hist_fast_12_slow_26_sig_9, macd_fast_6_slow_13_sig_5,' 'macd_signal_fast_6_slow_13_sig_5, macd_hist_fast_6_slow_13_sig_5,' 'macd_fast_18_slow_39_sig_14, macd_signal_fast_18_slow_39_sig_14,' 'macd_hist_fast_18_slow_39_sig_14, mesa_adaptive_ma_mama, mesa_adaptive_ma_fama,'    'money_flow_index_3_period, money_flow_index_10_period, money_flow_index_15_period,'    'money_flow_index_20_period, momentum_3_period, momentum_10_period, momentum_15_period,'    'momentum_20_period, normalized_atr_3_period, normalized_atr_10_period,'    'normalized_atr_15_period, normalized_atr_20_period, obv, percent_price_osc_fast_6_slow_13,' 'percent_price_osc_fast_12_slow_26, percent_price_osc_fast_18_slow_38, rsi_3_period,'    'rsi_10_period, rsi_15_period, rsi_20_period, parabolic_sar, parabolic_sar_ext,'    'std_deviation_3_period, std_deviation_10_period, std_deviation_15_period,'    'std_deviation_20_period, std_deviation_dbl_3_period, std_deviation_dbl_10_period,'    'std_deviation_dbl_15_period, std_deviation_dbl_20_period,'    'stochastic_sk_fast_5_slow_k_3_slow_d_3, stochastic_sd_fast_5_slow_k_3_slow_d_3,'    'stochastic_sk_fast_20_slow_k_7_slow_d_7, stochastic_sd_fast_20_slow_k_7_slow_d_7,'    'stochastic_sk_fast_20_slow_k_14_slow_d_14, stochastic_sd_fast_20_slow_k_14_slow_d_14,'    'triple_ema_3_period, triple_ema_10_period, triple_ema_15_period, true_range,'    'triangluar_ma_15_period, triangluar_ma_30_period, ultimate_osc_3_6_12_period, '   'ultimate_osc_7_14_28_period, ultimate_osc_10_20_40_period, williams_percent_r_3_period,'  'williams_percent_r_10_period, williams_percent_r_15_period, williams_percent_r_20_period,' 'weighted_ma_3_period, weighted_ma_10_period, weighted_ma_15_period,'    'weighted_ma_20_period) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['Fundamental_Indicators'] = ('INSERT INTO Fundamental_Indicators'
    '(transaction_id, total_revenue, cost_of_revenue, gross_profit, '
    'r_and_d, selling_gen_and_admin, operating_expense, operating_income, '
    'other_income_expense_net, ebit, intrest_income, pretax_income, '
    'income_tax, minority_intrest, net_income, net_income_basic,company_name, '
    'yr_high, yr_low, yr_change, shares_outstanding, shares_float, eps_ttm, '
    'dividend_yield, dividend_rate_ttm, employees, earnings_date, pe_ratio, '
    'beta, total_cash, current_debt, ebitda, revenue_per_share, '
    'revenue_per_employee, debt_to_equity, profit_margin, enterprise_value, '
    'enterprise_value_to_rev, price_to_sales, price_to_book, foward_pe_ratio, '
    'peg_ratio, pe_high, pe_low, depreciation, '
    'changes_in_receviables, changes_in_inventories, cash_change, cash_flow, '
    'capital_expenditures, investments, total_investing_cash_flows, '
    'dividends_paid, net_borrowings, other_cash_flows, cash_flow_financing, '
    'balance_sheet_date, current_cash, short_term_investments, receivables, '
    'inventory, other_current_assets, current_assets, long_term_investments, '
    'property_plant_equipment, goodwill, intangible_assets, other_assets, '
    'total_assets, accounts_payable, current_long_term_debt, '
    'other_current_liabilites, total_current_liabilites, long_term_debt, '
    'other_liabilites, minority_interest, total_liabilites, common_stock, '
    'retained_earnings, treasury_stock, capital_surplus, shareholder_equity,' 
    'net_tangible_assets, quick_ratio, current_ratio,total_debt_equity_ratio, '
    'long_term_debt_equity, short_term_debt_equity, '
    'intangibles_book_ratio, inventory_to_sales_ratio, '
    'long_term_debt_percent_invest_cap, short_term_debt_percent_invest_cap, '
    'long_term_debt_to_total_debt, short_term_debt_to_total_debt, '
    'total_liabilites_to_total_assets, working_capital,sector, sub_sector, '
    'institutional_ownership, short_interest_percent, '
    'avg_30_volume, mvg_avg_200, mvg_avg_50, max_change_percent, '
    'year_5_change_percent, year_2_change_percent, year_1_change_percent, '
    'ytd_change_percent, month_6_change_percent, month_3_change_percent, '
    'month_1_change_percent, day_30_change_percent, day_5_change_percent,  resistance_point_avg, resistance_point, support_point_avg, support_point, book_value ) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['Chart_Indicators'] = ('INSERT INTO Chart_Indicators (eod_id, '
    'two_crows, three_black_crows, three_inside_up_down,three_outside_up_down,'
    'three_line_strike, three_stars_south, three_adv_soliders, abandoned_baby,'
    'advance_block, belt_hold, breakaway, marubozu_closing, '
    'concealing_baby_swallow, counterattack, dark_cloud_cover,doji, doji_star,'
    'doji_dragonfly, engulfing_pattern, gravestone_doji, hammer, hanging_man, '
    'harami_pattern, harami_cross_pattern, high_wave_candle, hikkake_pattern,'
    'hikkake_mod_pattern,homing_pigeon,identical_three_crows, in_neck_pattern,'
    'inverted_hammer, kicking, ladder_bottom, doji_long_leg, long_line_candle,'
    'marubozu, matching_low, mat_hold, doji_morning_star, morning_star, '
    'on_neck_pattern, piercing_pattern, rickshaw_man, rise_fall_three_methods,'
    'seperating_lines, shooting_star, short_line_candle, spinning_top,'
    'stalled_pattern, stick_sandwhich, doji_tasuki, tasuki_gap, '
    'thrusting_pattern, tristar_pattern, three_unique_river, '
    'three_upside_gap_river ) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    '%s, %s, %s)')

    return INSERT_SQL

  
  # @params (None)
  # @descrip - The update statements that corresponds to correct model (aka db table). So when the cursor called, it provides the data and the insert statement provides the SQL. Not using yet. could just mirror the insert statement and update the whole row if we have all the values, which would be populated from the model.
  # @returns None
  def update_statements(self):
    UPDATE_SQL = {}
    return UPDATE_SQL


  # @params (None)
  # @descrip - The create table statements for all the tables in sectors
  # @returns None
  def sectors_tables(self):
    TABLES = {}

    TABLES['Sectors'] = (
    "CREATE TABLE IF NOT EXISTS `Sectors` ("
    "`sector_id` int(11) NOT NULL AUTO_INCREMENT,"
    "`date` date NOT NULL,"
    "`s_p` FLOAT(14, 4),"
    "`dji` FLOAT(14, 4),"
    "`nasdaq` FLOAT(14, 4),"
    "`russell_1000` FLOAT(14, 4),"
    "`russell_2000` FLOAT(14, 4),"
    "`vix` FLOAT(14, 4),"
    "`vix_close` FLOAT(14, 4),"
    "`real_estate` FLOAT(14, 4),"
    "`consumer_staples` FLOAT(14, 4),"
    "`health_care` FLOAT(14, 4),"
    "`utilities` FLOAT(14, 4),"
    "`materials` FLOAT(14, 4),"
    "`industrials` FLOAT(14, 4),"
    "`financials` FLOAT(14, 4),"
    "`energy` FLOAT(14, 4),"
    "`communication_services` FLOAT(14, 4),"
    "`consumer_discretionary` FLOAT(14, 4),"
    "`information_technology` FLOAT(14, 4),"
    "  PRIMARY KEY (`sector_id`)"
    ") ENGINE=InnoDB")

    return TABLES


  # @params (None)
  # @descrip - The create table statements for all the tables in nostradamus
  # @returns None
  def nostradamus_tables(self):
    TABLES = {}

    TABLES['Transaction'] = (
    "CREATE TABLE IF NOT EXISTS `Transaction` ("
    "`transaction_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`date` DATE NOT NULL,"
    "`ticker` VARCHAR(10),"
    "`percent_change` FLOAT(14, 4),"
    "  PRIMARY KEY (`transaction_id`)"
    ") ENGINE=InnoDB")

    TABLES['Price_EOD'] = (
    "CREATE TABLE IF NOT EXISTS `Price_EOD` ("
    "`eod_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`transaction_id` INT(11) NOT NULL,"
    "`date` DATE NOT NULL,"
    "`open` FLOAT(14, 4),"
    "`high` FLOAT(14, 4),"
    "`low` FLOAT(14, 4),"
    "`close` FLOAT(14, 4),"
    "`volume` FLOAT(14, 4),"
    "`percent_change` FLOAT(14, 4),"
    "`is_tracking_period` BOOLEAN,"
    "`avg_volume` FLOAT(14, 4)," 
    "  PRIMARY KEY (`eod_id`)"
    ") ENGINE=InnoDB")

    TABLES['Peer_Performance'] = (
    "CREATE TABLE IF NOT EXISTS `Peer_Performance` ("
    "`eod_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`transaction_id` INT(11) NOT NULL,"
    "`date` DATE NOT NULL,"
    "`open` FLOAT(14, 4),"
    "`high` FLOAT(14, 4),"
    "`low` FLOAT(14, 4),"
    "`close` FLOAT(14, 4),"
    "`volume` FLOAT(14, 4),"
    "`percent_change` FLOAT(14, 4),"
    "`ticker` TEXT NOT NULL,"
    "  PRIMARY KEY (`eod_id`)"
    ") ENGINE=InnoDB")

    TABLES['Price_Weekly'] = (
    "CREATE TABLE IF NOT EXISTS `Price_Weekly` ("
    "`weekly_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`transaction_id` INT(11) NOT NULL,"
    "`wk_start_date` DATE NOT NULL,"
    "`wk_end_date` DATE NOT NULL,"
    "`open` FLOAT(14, 4),"
    "`high` FLOAT(14, 4),"
    "`low` FLOAT(14, 4),"
    "`close` FLOAT(14, 4),"
    "`volume` FLOAT(14, 4),"
    "`avg_volume` FLOAT(14, 4),"
    "`percent_change` FLOAT(14, 4),"
    "  PRIMARY KEY (`weekly_id`)"
    ") ENGINE=InnoDB")

    TABLES['News_Event'] = (
    "CREATE TABLE IF NOT EXISTS `News_Event` ("
    "`news_event_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`transaction_id` INT(11) NOT NULL,"
    "`date_of_article` DATE NOT NULL,"
    "`title_of_article` TEXT,"
    "`link` TEXT,"
    "`source` TEXT,"
    "  PRIMARY KEY (`news_event_id`)"
    ") ENGINE=InnoDB")

    TABLES['SEC'] = (
    "CREATE TABLE IF NOT EXISTS `SEC` ("
    "`sec_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`transaction_id` INT(11) NOT NULL,"
    "`date_of_ipo` DATE,"
    "`late_filings` INT(11),"
    "`ct_orders` INT(11),"
    "`is_adr` BOOLEAN,"
    "  PRIMARY KEY (`sec_id`)"
    ") ENGINE=InnoDB")

    TABLES['SEC_Company_Info'] = (
    "CREATE TABLE IF NOT EXISTS `SEC_Company_Info` ("
    "`sec_company_info_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`sec_id` INT(11) NOT NULL,"
    "`date` DATE,"
    "`link` TEXT,"
    "`item_list` JSON,"
    "  PRIMARY KEY (`sec_company_info_id`)"
    ") ENGINE=InnoDB")

    TABLES['SEC_Merger'] = (
    "CREATE TABLE IF NOT EXISTS `SEC_Merger` ("
    "`sec_merger_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`sec_id` INT(11) NOT NULL,"
    "`date` DATE,"
    "`merging_with_company` TEXT,"
    "`merging_with_cik` INT(11),"
    "  PRIMARY KEY (`sec_merger_id`)"
    ") ENGINE=InnoDB")

    TABLES['SEC_Employee_Stock'] = (
    "CREATE TABLE IF NOT EXISTS `SEC_Employee_Stock` ("
    "`sec_employee_stock_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`sec_id` INT(11) NOT NULL,"
    "`date` DATE,"
    "`additional_shares_issued` INT(11),"
    "`link` TEXT,"
    "  PRIMARY KEY (`sec_employee_stock_id`)"
    ") ENGINE=InnoDB")

    TABLES['SEC_Secondary_Offering'] = (
    "CREATE TABLE IF NOT EXISTS `SEC_Secondary_Offering` ("
    "`sec_secondary_offering_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`sec_id` INT(11) NOT NULL,"
    "`date` DATE,"
    "`additional_shares_issued` INT(11),"
    "`is_asr` BOOLEAN,"
    "`link` TEXT,"
    "  PRIMARY KEY (`sec_secondary_offering_id`)"
    ") ENGINE=InnoDB")

    TABLES['Technical_Indicators'] = (
    "CREATE TABLE IF NOT EXISTS `Technical_Indicators` ("
    "`eod_id` INT(11) NOT NULL,"
    "`atr_3_period` FLOAT(14, 4),"
    "`atr_10_period` FLOAT(14, 4),"
    "`atr_15_period` FLOAT(14, 4),"
    "`atr_20_period` FLOAT(14, 4),"
    "`boll_bands_upper_3_period` FLOAT(14, 4),"
    "`boll_bands_middle_3_period` FLOAT(14, 4),"
    "`boll_bands_lower_3_period` FLOAT(14, 4),"
    "`boll_bands_upper_10_period` FLOAT(14, 4),"
    "`boll_bands_middle_10_period` FLOAT(14, 4),"
    "`boll_bands_lower_10_period` FLOAT(14, 4),"
    "`boll_bands_upper_15_period` FLOAT(14, 4),"
    "`boll_bands_middle_15_period` FLOAT(14, 4),"
    "`boll_bands_lower_15_period` FLOAT(14, 4),"
    "`boll_bands_upper_20_period` FLOAT(14, 4),"
    "`boll_bands_middle_20_period` FLOAT(14, 4),"
    "`boll_bands_lower_20_period` FLOAT(14, 4),"
    "`sma_3_period` FLOAT(14, 4),"
    "`sma_10_period` FLOAT(14, 4),"
    "`sma_15_period` FLOAT(14, 4),"
    "`sma_20_period` FLOAT(14, 4),"
    "`ema_3_period` FLOAT(14, 4),"
    "`ema_10_period` FLOAT(14, 4),"
    "`ema_15_period` FLOAT(14, 4),"
    "`ema_20_period` FLOAT(14, 4),"
    "`average_directional_movement_3_period` FLOAT(14, 4),"
    "`average_directional_movement_10_period` FLOAT(14, 4),"
    "`average_directional_movement_15_period` FLOAT(14, 4),"
    "`average_directional_movement_20_period` FLOAT(14, 4),"
    "`chaikin_osc_fast_3_slow_10` FLOAT(14, 4),"
    "`chaikin_osc_fast_6_slow_18` FLOAT(14, 4),"
    "`chaikin_osc_fast_10_slow_20` FLOAT(14, 4),"
    "`chaikin_a_d_line` FLOAT(14, 4),"
    "`balance_of_power` FLOAT(14, 4),"
    "`commodity_channel_index_3_period` FLOAT(14, 4),"
    "`commodity_channel_index_10_period` FLOAT(14, 4),"
    "`commodity_channel_index_15_period` FLOAT(14, 4),"
    "`commodity_channel_index_20_period` FLOAT(14, 4),"
    "`chande_momentum_oscillator_3_period` FLOAT(14, 4),"
    "`chande_momentum_oscillator_10_period` FLOAT(14, 4),"
    "`chande_momentum_oscillator_15_period` FLOAT(14, 4),"
    "`chande_momentum_oscillator_20_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_vol_5_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_vol_15_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_vol_30_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_avg_vol_5_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_avg_vol_15_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_avg_vol_30_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_sp_5_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_sp_15_period` FLOAT(14, 4),"
    "`pearsons_coeff_close_sp_30_period` FLOAT(14, 4),"
    "`double_ema_3_period` FLOAT(14, 4),"
    "`double_ema_10_period` FLOAT(14, 4),"
    "`double_ema_15_period` FLOAT(14, 4),"
    "`double_ema_20_period` FLOAT(14, 4),"
    "`directional_movement_index_3_period` FLOAT(14, 4),"
    "`directional_movement_index_10_period` FLOAT(14, 4),"
    "`directional_movement_index_15_period` FLOAT(14, 4),"
    "`directional_movement_index_20_period` FLOAT(14, 4),"
    "`kaufman_adaptive_ma_5_period` FLOAT(14, 4),"
    "`kaufman_adaptive_ma_15_period` FLOAT(14, 4),"
    "`kaufman_adaptive_ma_30_period` FLOAT(14, 4),"
    "`linear_reg_3_period` FLOAT(14, 4),"
    "`linear_reg_10_period` FLOAT(14, 4),"
    "`linear_reg_15_period` FLOAT(14, 4),"
    "`linear_reg_20_period` FLOAT(14, 4),"
    "`linear_reg_angle_3_period` FLOAT(14, 4),"
    "`linear_reg_angle_10_period` FLOAT(14, 4),"
    "`linear_reg_angle_15_period` FLOAT(14, 4),"
    "`linear_reg_angle_20_period` FLOAT(14, 4),"
    "`linear_reg_intercept_3_period` FLOAT(14, 4),"
    "`linear_reg_intercept_10_period` FLOAT(14, 4),"
    "`linear_reg_intercept_15_period` FLOAT(14, 4),"
    "`linear_reg_intercept_20_period` FLOAT(14, 4),"
    "`linear_reg_slope_3_period` FLOAT(14, 4),"
    "`linear_reg_slope_10_period` FLOAT(14, 4),"
    "`linear_reg_slope_15_period` FLOAT(14, 4),"
    "`linear_reg_slope_20_period` FLOAT(14, 4),"
    "`macd_fast_12_slow_26_sig_9` FLOAT(14, 4),"
    "`macd_signal_fast_12_slow_26_sig_9` FLOAT(14, 4),"
    "`macd_hist_fast_12_slow_26_sig_9` FLOAT(14, 4),"
    "`macd_fast_6_slow_13_sig_5` FLOAT(14, 4),"
    "`macd_signal_fast_6_slow_13_sig_5` FLOAT(14, 4),"
    "`macd_hist_fast_6_slow_13_sig_5` FLOAT(14, 4),"
    "`macd_fast_18_slow_39_sig_14` FLOAT(14, 4),"
    "`macd_signal_fast_18_slow_39_sig_14` FLOAT(14, 4),"
    "`macd_hist_fast_18_slow_39_sig_14` FLOAT(14, 4),"
    "`mesa_adaptive_ma_mama` FLOAT(14, 4),"
    "`mesa_adaptive_ma_fama` FLOAT(14, 4),"
    "`money_flow_index_3_period` FLOAT(14, 4),"
    "`money_flow_index_10_period` FLOAT(14, 4),"
    "`money_flow_index_15_period` FLOAT(14, 4),"
    "`money_flow_index_20_period` FLOAT(14, 4),"
    "`momentum_3_period` FLOAT(14, 4),"
    "`momentum_10_period` FLOAT(14, 4),"
    "`momentum_15_period` FLOAT(14, 4),"
    "`momentum_20_period` FLOAT(14, 4),"
    "`normalized_atr_3_period` FLOAT(14, 4),"
    "`normalized_atr_10_period` FLOAT(14, 4),"
    "`normalized_atr_15_period` FLOAT(14, 4),"
    "`normalized_atr_20_period` FLOAT(14, 4),"
    "`obv` FLOAT(14, 4),"
    "`percent_price_osc_fast_6_slow_13` FLOAT(14, 4),"
    "`percent_price_osc_fast_12_slow_26` FLOAT(14, 4),"
    "`percent_price_osc_fast_18_slow_38` FLOAT(14, 4),"
    "`rsi_3_period` FLOAT(14, 4),"
    "`rsi_10_period` FLOAT(14, 4),"
    "`rsi_15_period` FLOAT(14, 4),"
    "`rsi_20_period` FLOAT(14, 4),"
    "`parabolic_sar` FLOAT(14, 4),"
    "`parabolic_sar_ext` FLOAT(14, 4),"
    "`std_deviation_3_period` FLOAT(14, 4),"
    "`std_deviation_10_period` FLOAT(14, 4),"
    "`std_deviation_15_period` FLOAT(14, 4),"
    "`std_deviation_20_period` FLOAT(14, 4),"
    "`std_deviation_dbl_3_period` FLOAT(14, 4),"
    "`std_deviation_dbl_10_period` FLOAT(14, 4),"
    "`std_deviation_dbl_15_period` FLOAT(14, 4),"
    "`std_deviation_dbl_20_period` FLOAT(14, 4),"
    "`stochastic_sk_fast_5_slow_k_3_slow_d_3` FLOAT(14, 4),"
    "`stochastic_sd_fast_5_slow_k_3_slow_d_3` FLOAT(14, 4),"
    "`stochastic_sk_fast_20_slow_k_7_slow_d_7` FLOAT(14, 4),"
    "`stochastic_sd_fast_20_slow_k_7_slow_d_7` FLOAT(14, 4),"
    "`stochastic_sk_fast_20_slow_k_14_slow_d_14` FLOAT(14, 4),"
    "`stochastic_sd_fast_20_slow_k_14_slow_d_14` FLOAT(14, 4),"
    "`triple_ema_3_period` FLOAT(14, 4),"
    "`triple_ema_10_period` FLOAT(14, 4),"
    "`triple_ema_15_period` FLOAT(14, 4),"
    "`true_range` FLOAT(14, 4),"
    "`triangluar_ma_15_period` FLOAT(14, 4),"
    "`triangluar_ma_30_period` FLOAT(14, 4),"
    "`ultimate_osc_3_6_12_period` FLOAT(14, 4),"
    "`ultimate_osc_7_14_28_period` FLOAT(14, 4),"
    "`ultimate_osc_10_20_40_period` FLOAT(14, 4),"
    "`williams_percent_r_3_period` FLOAT(14, 4),"
    "`williams_percent_r_10_period` FLOAT(14, 4),"
    "`williams_percent_r_15_period` FLOAT(14, 4),"
    "`williams_percent_r_20_period` FLOAT(14, 4),"
    "`weighted_ma_3_period` FLOAT(14, 4),"
    "`weighted_ma_10_period` FLOAT(14, 4),"
    "`weighted_ma_15_period` FLOAT(14, 4),"
    "`weighted_ma_20_period` FLOAT(14, 4),"
    "  CONSTRAINT `tech_indc_ibfk_1` FOREIGN KEY (`eod_id`) "
    "     REFERENCES `Price_EOD` (`eod_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

    TABLES['Fundamental_Indicators'] = (
    "CREATE TABLE IF NOT EXISTS `Fundamental_Indicators` ("
    "`transaction_id` INT(11) NOT NULL,"
    "`total_revenue` FLOAT(14, 4) ,"
    "`cost_of_revenue` FLOAT(14, 4) ,"
    "`gross_profit` FLOAT(14, 4) ,"
    "`r_and_d` FLOAT(14, 4) ,"
    "`selling_gen_and_admin` FLOAT(14, 4) ,"
    "`operating_expense` FLOAT(14, 4) ,"
    "`operating_income` FLOAT(14, 4) ,"
    "`other_income_expense_net` FLOAT(14, 4) ,"
    "`ebit` FLOAT(14, 4) ,"
    "`intrest_income` FLOAT(14, 4) ,"
    "`pretax_income` FLOAT(14, 4) ,"
    "`income_tax` FLOAT(14, 4) ,"
    "`minority_intrest` FLOAT(14, 4) ,"
    "`net_income` FLOAT(14, 4) ,"
    "`net_income_basic` FLOAT(14, 4) ,"
    "`company_name` TINYTEXT,"
    "`yr_high` FLOAT(14, 4) ,"
    "`yr_low` FLOAT(14, 4) ,"
    "`yr_change` FLOAT(14, 4) ,"
    "`shares_outstanding` FLOAT(14, 4) ,"
    "`shares_float` FLOAT(14, 4) ,"
    "`eps_ttm` FLOAT(14, 4) ,"
    "`dividend_yield` FLOAT(14, 4) ,"
    "`dividend_rate_ttm` FLOAT(14, 4) ,"
    "`employees` FLOAT(14, 4) ,"
    "`earnings_date` DATE,"
    "`pe_ratio` FLOAT(14, 4) ,"
    "`beta` FLOAT(14, 4) ,"
    "`total_cash` FLOAT(14, 4) ,"
    "`current_debt` FLOAT(14, 4) ,"
    "`ebitda` FLOAT(14, 4) ,"
    "`revenue_per_share` FLOAT(14, 4) ,"
    "`revenue_per_employee` FLOAT(14, 4) ,"
    "`debt_to_equity` FLOAT(14, 4) ,"
    "`profit_margin` FLOAT(14, 4) ,"
    "`enterprise_value` FLOAT(14, 4) ,"
    "`enterprise_value_to_rev` FLOAT(14, 4) ,"
    "`price_to_sales` FLOAT(14, 4) ,"
    "`price_to_book` FLOAT(14, 4) ,"
    "`foward_pe_ratio` FLOAT(14, 4) ,"
    "`peg_ratio` FLOAT(14, 4) ,"
    "`pe_high` FLOAT(14, 4) ,"
    "`pe_low` FLOAT(14, 4) ,"
    "`depreciation` FLOAT(14, 4) ,"
    "`changes_in_receviables` FLOAT(14, 4) ,"
    "`changes_in_inventories` FLOAT(14, 4) ,"
    "`cash_change` FLOAT(14, 4) ,"
    "`cash_flow` FLOAT(14, 4) ,"
    "`capital_expenditures` FLOAT(14, 4) ,"
    "`investments` FLOAT(14, 4) ,"
    "`total_investing_cash_flows` FLOAT(14, 4) ,"
    "`dividends_paid` FLOAT(14, 4) ,"
    "`net_borrowings` FLOAT(14, 4) ,"
    "`other_cash_flows` FLOAT(14, 4) ,"
    "`cash_flow_financing` FLOAT(14, 4) ,"
    "`balance_sheet_date` DATE,"
    "`current_cash` FLOAT(14, 4) ,"
    "`short_term_investments` FLOAT(14, 4) ,"
    "`receivables` FLOAT(14, 4) ,"
    "`inventory` FLOAT(14, 4) ,"
    "`other_current_assets` FLOAT(14, 4) ,"
    "`current_assets` FLOAT(14, 4) ,"
    "`long_term_investments` FLOAT(14, 4) ,"
    "`property_plant_equipment` FLOAT(14, 4) ,"
    "`goodwill` FLOAT(14, 4) ,"
    "`intangible_assets` FLOAT(14, 4) ,"
    "`other_assets` FLOAT(14, 4) ,"
    "`total_assets` FLOAT(14, 4) ,"
    "`accounts_payable` FLOAT(14, 4) ,"
    "`current_long_term_debt` FLOAT(14, 4) ,"
    "`other_current_liabilites` FLOAT(14, 4) ,"
    "`total_current_liabilites` FLOAT(14, 4) ,"
    "`long_term_debt` FLOAT(14, 4) ,"
    "`other_liabilites` FLOAT(14, 4) ,"
    "`minority_interest` FLOAT(14, 4) ,"
    "`total_liabilites` FLOAT(14, 4) ,"
    "`common_stock` FLOAT(14, 4) ,"
    "`retained_earnings` FLOAT(14, 4) ,"
    "`treasury_stock` FLOAT(14, 4) ,"
    "`capital_surplus` FLOAT(14, 4) ,"
    "`shareholder_equity` FLOAT(14, 4) ,"
    "`net_tangible_assets` FLOAT(14, 4) ,"
    "`quick_ratio` FLOAT(14, 4) ,"
    "`current_ratio` FLOAT(14, 4) ,"
    "`total_debt_equity_ratio` FLOAT(14, 4) ,"
    "`long_term_debt_equity` FLOAT(14, 4) ,"
    "`short_term_debt_equity` FLOAT(14, 4) ,"
    "`intangibles_book_ratio` FLOAT(14, 4) ,"
    "`inventory_to_sales_ratio` FLOAT(14, 4) ,"
    "`long_term_debt_percent_invest_cap` FLOAT(14, 4) ,"
    "`short_term_debt_percent_invest_cap` FLOAT(14, 4) ,"
    "`long_term_debt_to_total_debt` FLOAT(14, 4) ,"
    "`short_term_debt_to_total_debt` FLOAT(14, 4) ,"
    "`total_liabilites_to_total_assets` FLOAT(14, 4) ,"
    "`working_capital` FLOAT(14, 4) ,"
    "`sector` TEXT,"
    "`sub_sector` TEXT,"
    "`institutional_ownership` FLOAT(14, 4) ,"
    "`short_interest_percent` FLOAT(14, 4),"
    "`avg_30_volume` FLOAT(14, 4) ,"
    "`mvg_avg_200` FLOAT(14, 4) ,"
    "`mvg_avg_50` FLOAT(14, 4) ,"
    "`max_change_percent` FLOAT(14, 4) ,"
    "`year_5_change_percent` FLOAT(14, 4) ,"
    "`year_2_change_percent` FLOAT(14, 4) ,"
    "`year_1_change_percent` FLOAT(14, 4) ,"
    "`ytd_change_percent` FLOAT(14, 4) ,"
    "`month_6_change_percent` FLOAT(14, 4) ,"
    "`month_3_change_percent` FLOAT(14, 4) ,"
    "`month_1_change_percent` FLOAT(14, 4) ,"
    "`day_30_change_percent` FLOAT(14, 4) ,"
    "`day_5_change_percent` FLOAT(14, 4) ,"
    "`resistance_point_avg` FLOAT(14, 4),"
    "`resistance_point` FLOAT(14, 4),"
    "`support_point` FLOAT(14, 4),"
    "`support_point_avg` FLOAT(14, 4),"
    "`book_value` FLOAT(14, 4),"
    "  CONSTRAINT `fund_indc_ibfk_1` FOREIGN KEY (`transaction_id`) "
    "     REFERENCES `Transaction` (`transaction_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

    TABLES['Chart_Indicators'] = (
    "CREATE TABLE IF NOT EXISTS `Chart_Indicators` ("
    "`eod_id` INT(11) NOT NULL,"
    "`two_crows` INT(11),"
    "`three_black_crows` INT(11),"
    "`three_inside_up_down` INT(11),"
    "`three_outside_up_down` INT(11),"
    "`three_line_strike` INT(11),"
    "`three_stars_south` INT(11),"
    "`three_adv_soliders` INT(11),"
    "`abandoned_baby` INT(11),"
    "`advance_block` INT(11),"
    "`belt_hold` INT(11),"
    "`breakaway` INT(11),"
    "`marubozu_closing` INT(11),"
    "`concealing_baby_swallow` INT(11),"
    "`counterattack` INT(11),"
    "`dark_cloud_cover` INT(11),"
    "`doji` INT(11),"
    "`doji_star` INT(11),"
    "`doji_dragonfly` INT(11),"
    "`engulfing_pattern` INT(11),"
    "`gravestone_doji` INT(11),"
    "`hammer` INT(11),"
    "`hanging_man` INT(11),"
    "`harami_pattern` INT(11),"
    "`harami_cross_pattern` INT(11),"
    "`high_wave_candle` INT(11),"
    "`hikkake_pattern` INT(11),"
    "`hikkake_mod_pattern` INT(11),"
    "`homing_pigeon` INT(11),"
    "`identical_three_crows` INT(11),"
    "`in_neck_pattern` INT(11),"
    "`inverted_hammer` INT(11),"
    "`kicking` INT(11),"
    "`ladder_bottom` INT(11),"
    "`doji_long_leg` INT(11),"
    "`long_line_candle` INT(11),"
    "`marubozu` INT(11),"
    "`matching_low` INT(11),"
    "`mat_hold` INT(11),"
    "`doji_morning_star` INT(11),"
    "`morning_star` INT(11),"
    "`on_neck_pattern` INT(11),"
    "`piercing_pattern` INT(11),"
    "`rickshaw_man` INT(11),"
    "`rise_fall_three_methods` INT(11),"
    "`seperating_lines` INT(11),"
    "`shooting_star` INT(11),"
    "`short_line_candle` INT(11),"
    "`spinning_top` INT(11),"
    "`stalled_pattern` INT(11),"
    "`stick_sandwhich` INT(11),"
    "`doji_tasuki` INT(11),"
    "`tasuki_gap` INT(11),"
    "`thrusting_pattern` INT(11),"
    "`tristar_pattern` INT(11),"
    "`three_unique_river` INT(11),"
    "`three_upside_gap_river` INT(11),"
    "  CONSTRAINT `chart_indc_ibfk_1` FOREIGN KEY (`eod_id`) "
    "     REFERENCES `Price_EOD` (`eod_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")            

    return TABLES
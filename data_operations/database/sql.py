
class DB_SCHEMA(object):

  def __init__(self):
    self.DB_NAME = 'nostradamus'
    return

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
    'date, transaction_id, is_tracking_period, '
    'open, high, low, close, volume, avg_volume, percent_change) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['Price_Weekly'] = ('INSERT INTO Price_Weekly ('
    'transaction_id, wk_start_date, wk_end_date, open, high, '
    'low, close, volume, avg_volume, percent_change) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    INSERT_SQL['Technical_Indicators'] = ('INSERT INTO Technical_Indicators ('
    'eod_id, atr, boll_bands, sma, ema, average_directional_movement, chaikin_osc, '
    'chaikin_a_d_line, balance_of_power, commodity_channel_index, '
    'chande_momentum_oscillator, pearsons_coefficient, double_ema, '
    'directional_movement_index, kaufman_adaptive_ma, linear_reg, '
    'linear_reg_angle, linear_reg_intercept, linear_reg_slope, '
    'macd_conv_diver, mesa_adaptive_ma, money_flow_index, momentum, '
    'normalized_atr, obv, percent_price_osc, rsi, parabolic_sar,'
    'parabolic_sar_ext, std_deviation, stochastic, stochastic_fast, '
    'stochastic_rsi, triple_ema, true_range, triangluar_ma, ultimate_osc, '
    'williams_percent_r, weighted_ma, resistance_point, support_point) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    ' %s, %s, %s, %s, %s)')

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
    'long_term_debt_equity, short_term_debt_equity, avg_age_of_inventory, '
    'intangibles_book_ratio, inventory_to_sales_ratio, '
    'long_term_debt_percent_invest_cap, short_term_debt_percent_invest_cap, '
    'long_term_debt_to_total_debt, short_term_debt_to_total_debt, '
    'total_liabilites_to_total_assets, working_capital,sector, sector_change,' 
    'avg_30_volume, mvg_avg_200, mvg_avg_50, max_change_percent, '
    'year_5_change_percent, year_2_change_percent, year_1_change_percent, '
    'ytd_change_percent, month_6_change_percent, month_3_change_percent, '
    'month_1_change_percent, day_30_change_percent, day_5_change_percent ) VALUES '
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
    '%s, %s, %s, %s, %s, %s, %s)')

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

  def update_statements(self):
    UPDATE_SQL = {}
    return UPDATE_SQL

  def tables(self):
    TABLES = {}

    TABLES['Sectors'] = (
    "CREATE TABLE IF NOT EXISTS `Sectors` ("
    "`sector_id` int(11) NOT NULL AUTO_INCREMENT,"
    "`date` date NOT NULL,"
    "`s_p` float,"
    "`dji` float,"
    "`nasdaq` float,"
    "`russell_1000` float,"
    "`russell_2000` float,"
    "`vix` float,"
    "`vix_close` float,"
    "`real_estate` float,"
    "`consumer_staples` float,"
    "`health_care` float,"
    "`utilities` float,"
    "`materials` float,"
    "`industrials` float,"
    "`financials` float,"
    "`energy` float,"
    "`communication_services` float,"
    "`consumer_discretionary` float,"
    "`information_technology` float,"
    "  PRIMARY KEY (`sector_id`)"
    ") ENGINE=InnoDB")

    TABLES['Transaction'] = (
    "CREATE TABLE IF NOT EXISTS `Transaction` ("
    "`transaction_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`date` DATE NOT NULL,"
    "`ticker` VARCHAR(10),"
    "`percent_change` FLOAT,"
    "  PRIMARY KEY (`transaction_id`)"
    ") ENGINE=InnoDB")

    TABLES['Price_EOD'] = (
    "CREATE TABLE IF NOT EXISTS `Price_EOD` ("
    "`eod_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`date` DATE NOT NULL,"
    "`transaction_id` INT(11) NOT NULL,"
    "`is_tracking_period` BOOLEAN,"
    "`open` FLOAT,"
    "`high` FLOAT,"
    "`low` FLOAT,"
    "`close` FLOAT,"
    "`volume` FLOAT,"
    "`avg_volume` FLOAT,"
    "`percent_change` FLOAT,"
    "  PRIMARY KEY (`eod_id`)"
    ") ENGINE=InnoDB")

    TABLES['Price_Weekly'] = (
    "CREATE TABLE IF NOT EXISTS `Price_Weekly` ("
    "`weekly_id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`transaction_id` INT(11) NOT NULL,"
    "`wk_start_date` DATE NOT NULL,"
    "`wk_end_date` DATE NOT NULL,"
    "`open` FLOAT,"
    "`high` FLOAT,"
    "`low` FLOAT,"
    "`close` FLOAT,"
    "`volume` FLOAT,"
    "`avg_volume` FLOAT,"
    "`percent_change` FLOAT,"
    "  PRIMARY KEY (`weekly_id`)"
    ") ENGINE=InnoDB")

    TABLES['Technical_Indicators'] = (
    "CREATE TABLE IF NOT EXISTS `Technical_Indicators` ("
    "`eod_id` INT(11) NOT NULL,"
    "`atr` FLOAT,"
    "`boll_bands` FLOAT,"
    "`sma` FLOAT,"
    "`ema` FLOAT,"
    "`average_directional_movement` FLOAT,"
    "`chaikin_osc` FLOAT,"
    "`chaikin_a_d_line` FLOAT,"
    "`balance_of_power` FLOAT,"
    "`commodity_channel_index` FLOAT,"
    "`chande_momentum_oscillator` FLOAT,"
    "`pearsons_coefficient` FLOAT,"
    "`double_ema` FLOAT,"
    "`directional_movement_index` FLOAT,"
    "`kaufman_adaptive_ma` FLOAT,"
    "`linear_reg` FLOAT,"
    "`linear_reg_angle` FLOAT,"
    "`linear_reg_intercept` FLOAT,"
    "`linear_reg_slope` FLOAT,"
    "`macd_conv_diver` FLOAT,"
    "`mesa_adaptive_ma` FLOAT,"
    "`money_flow_index` FLOAT,"
    "`momentum`  FLOAT,"
    "`normalized_atr` FLOAT,"
    "`obv` FLOAT,"
    "`percent_price_osc` FLOAT,"
    "`rsi` FLOAT,"
    "`parabolic_sar` FLOAT,"
    "`parabolic_sar_ext` FLOAT,"
    "`std_deviation` FLOAT,"
    "`stochastic` FLOAT,"
    "`stochastic_fast` FLOAT,"
    "`stochastic_rsi` FLOAT,"
    "`triple_ema` FLOAT,"
    "`true_range` FLOAT,"
    "`triangluar_ma` FLOAT,"
    "`ultimate_osc` FLOAT,"
    "`williams_percent_r` FLOAT,"
    "`weighted_ma` FLOAT,"
    "`resistance_point` FLOAT,"
    "`support_point` FLOAT,"
    "  CONSTRAINT `tech_indc_ibfk_1` FOREIGN KEY (`eod_id`) "
    "     REFERENCES `Price_EOD` (`eod_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

    TABLES['Fundamental_Indicators'] = (
    "CREATE TABLE IF NOT EXISTS `Fundamental_Indicators` ("
    "`transaction_id` INT(11) NOT NULL,"
    "`total_revenue` FLOAT ,"
    "`cost_of_revenue` FLOAT ,"
    "`gross_profit` FLOAT ,"
    "`r_and_d` FLOAT ,"
    "`selling_gen_and_admin` FLOAT ,"
    "`operating_expense` FLOAT ,"
    "`operating_income` FLOAT ,"
    "`other_income_expense_net` FLOAT ,"
    "`ebit` FLOAT ,"
    "`intrest_income` FLOAT ,"
    "`pretax_income` FLOAT ,"
    "`income_tax` FLOAT ,"
    "`minority_intrest` FLOAT ,"
    "`net_income` FLOAT ,"
    "`net_income_basic` FLOAT ,"
    "`company_name` TINYTEXT,"
    "`yr_high` FLOAT ,"
    "`yr_low` FLOAT ,"
    "`yr_change` FLOAT ,"
    "`shares_outstanding` FLOAT ,"
    "`shares_float` FLOAT ,"
    "`eps_ttm` FLOAT ,"
    "`dividend_yield` FLOAT ,"
    "`dividend_rate_ttm` FLOAT ,"
    "`employees` FLOAT ,"
    "`earnings_date` DATE,"
    "`pe_ratio` FLOAT ,"
    "`beta` FLOAT ,"
    "`total_cash` FLOAT ,"
    "`current_debt` FLOAT ,"
    "`ebitda` FLOAT ,"
    "`revenue_per_share` FLOAT ,"
    "`revenue_per_employee` FLOAT ,"
    "`debt_to_equity` FLOAT ,"
    "`profit_margin` FLOAT ,"
    "`enterprise_value` FLOAT ,"
    "`enterprise_value_to_rev` FLOAT ,"
    "`price_to_sales` FLOAT ,"
    "`price_to_book` FLOAT ,"
    "`foward_pe_ratio` FLOAT ,"
    "`peg_ratio` FLOAT ,"
    "`pe_high` FLOAT ,"
    "`pe_low` FLOAT ,"
    "`depreciation` FLOAT ,"
    "`changes_in_receviables` FLOAT ,"
    "`changes_in_inventories` FLOAT ,"
    "`cash_change` FLOAT ,"
    "`cash_flow` FLOAT ,"
    "`capital_expenditures` FLOAT ,"
    "`investments` FLOAT ,"
    "`total_investing_cash_flows` FLOAT ,"
    "`dividends_paid` FLOAT ,"
    "`net_borrowings` FLOAT ,"
    "`other_cash_flows` FLOAT ,"
    "`cash_flow_financing` FLOAT ,"
    "`balance_sheet_date` DATE,"
    "`current_cash` FLOAT ,"
    "`short_term_investments` FLOAT ,"
    "`receivables` FLOAT ,"
    "`inventory` FLOAT ,"
    "`other_current_assets` FLOAT ,"
    "`current_assets` FLOAT ,"
    "`long_term_investments` FLOAT ,"
    "`property_plant_equipment` FLOAT ,"
    "`goodwill` FLOAT ,"
    "`intangible_assets` FLOAT ,"
    "`other_assets` FLOAT ,"
    "`total_assets` FLOAT ,"
    "`accounts_payable` FLOAT ,"
    "`current_long_term_debt` FLOAT ,"
    "`other_current_liabilites` FLOAT ,"
    "`total_current_liabilites` FLOAT ,"
    "`long_term_debt` FLOAT ,"
    "`other_liabilites` FLOAT ,"
    "`minority_interest` FLOAT ,"
    "`total_liabilites` FLOAT ,"
    "`common_stock` FLOAT ,"
    "`retained_earnings` FLOAT ,"
    "`treasury_stock` FLOAT ,"
    "`capital_surplus` FLOAT ,"
    "`shareholder_equity` FLOAT ,"
    "`net_tangible_assets` FLOAT ,"
    "`quick_ratio` FLOAT ,"
    "`current_ratio` FLOAT ,"
    "`total_debt_equity_ratio` FLOAT ,"
    "`long_term_debt_equity` FLOAT ,"
    "`short_term_debt_equity` FLOAT ,"
    "`avg_age_of_inventory` FLOAT ,"
    "`intangibles_book_ratio` FLOAT ,"
    "`inventory_to_sales_ratio` FLOAT ,"
    "`long_term_debt_percent_invest_cap` FLOAT ,"
    "`short_term_debt_percent_invest_cap` FLOAT ,"
    "`long_term_debt_to_total_debt` FLOAT ,"
    "`short_term_debt_to_total_debt` FLOAT ,"
    "`total_liabilites_to_total_assets` FLOAT ,"
    "`working_capital` FLOAT ,"
    "`sector` TEXT,"
    "`sector_change` FLOAT ,"
    "`avg_30_volume` FLOAT ,"
    "`mvg_avg_200` FLOAT ,"
    "`mvg_avg_50` FLOAT ,"
    "`max_change_percent` FLOAT ,"
    "`year_5_change_percent` FLOAT ,"
    "`year_2_change_percent` FLOAT ,"
    "`year_1_change_percent` FLOAT ,"
    "`ytd_change_percent` FLOAT ,"
    "`month_6_change_percent` FLOAT ,"
    "`month_3_change_percent` FLOAT ,"
    "`month_1_change_percent` FLOAT ,"
    "`day_30_change_percent` FLOAT ,"
    "`day_5_change_percent` FLOAT ,"
    "  CONSTRAINT `fund_indc_ibfk_1` FOREIGN KEY (`transaction_id`) "
    "     REFERENCES `Transaction` (`transaction_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

    TABLES['Chart_Indicators'] = (
    "CREATE TABLE IF NOT EXISTS `Chart_Indicators` ("
    "`eod_id` INT(11) NOT NULL,"
    "`two_crows` FLOAT,"
    "`three_black_crows` FLOAT,"
    "`three_inside_up_down` FLOAT,"
    "`three_outside_up_down` FLOAT,"
    "`three_line_strike` FLOAT,"
    "`three_stars_south` FLOAT,"
    "`three_adv_soliders` FLOAT,"
    "`abandoned_baby` FLOAT,"
    "`advance_block` FLOAT,"
    "`belt_hold` FLOAT,"
    "`breakaway` FLOAT,"
    "`marubozu_closing` FLOAT,"
    "`concealing_baby_swallow` FLOAT,"
    "`counterattack` FLOAT,"
    "`dark_cloud_cover` FLOAT,"
    "`doji` FLOAT,"
    "`doji_star` FLOAT,"
    "`doji_dragonfly` FLOAT,"
    "`engulfing_pattern` FLOAT,"
    "`gravestone_doji` FLOAT,"
    "`hammer` FLOAT,"
    "`hanging_man` FLOAT,"
    "`harami_pattern` FLOAT,"
    "`harami_cross_pattern` FLOAT,"
    "`high_wave_candle` FLOAT,"
    "`hikkake_pattern` FLOAT,"
    "`hikkake_mod_pattern` FLOAT,"
    "`homing_pigeon` FLOAT,"
    "`identical_three_crows` FLOAT,"
    "`in_neck_pattern` FLOAT,"
    "`inverted_hammer` FLOAT,"
    "`kicking` FLOAT,"
    "`ladder_bottom` FLOAT,"
    "`doji_long_leg` FLOAT,"
    "`long_line_candle` FLOAT,"
    "`marubozu` FLOAT,"
    "`matching_low` FLOAT,"
    "`mat_hold` FLOAT,"
    "`doji_morning_star` FLOAT,"
    "`morning_star` FLOAT,"
    "`on_neck_pattern` FLOAT,"
    "`piercing_pattern` FLOAT,"
    "`rickshaw_man` FLOAT,"
    "`rise_fall_three_methods` FLOAT,"
    "`seperating_lines` FLOAT,"
    "`shooting_star` FLOAT,"
    "`short_line_candle` FLOAT,"
    "`spinning_top` FLOAT,"
    "`stalled_pattern` FLOAT,"
    "`stick_sandwhich` FLOAT,"
    "`doji_tasuki` FLOAT,"
    "`tasuki_gap` FLOAT,"
    "`thrusting_pattern` FLOAT,"
    "`tristar_pattern` FLOAT,"
    "`three_unique_river` FLOAT,"
    "`three_upside_gap_river` FLOAT,"
    "  CONSTRAINT `chart_indc_ibfk_1` FOREIGN KEY (`eod_id`) "
    "     REFERENCES `Price_EOD` (`eod_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")            

    return TABLES
    
    
    
    '''
    "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
    '''
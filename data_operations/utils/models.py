from utils.helpers import Base_Model
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
#                Transaction Table                        #
# ======================================================= #

class Transaction(Base_Model):

  def __init__(self):
    self.transaction_id = -1
    self.date = ''
    self.ticker = ''
    self.sector_change = 0
    self.percent_change = super().initial_float
    return



# ======================================================= #
#    Price End of Day - Transaction Bridge Table          #
# ======================================================= #

class PEOD_Transact_Bridge(Base_Model):

  def __init__(self):
    self.row_id = -1
    self.transaction_id = -1
    self.eod_id = -1
    return

# ======================================================= #
#                Price End of Day Table                   #
# ======================================================= #

class Price_EOD(Base_Model):

  def __init__(self):
    self.eod_id = -1
    self.is_tracking_period = True
    self.open = -1
    self.high = -1
    self.low = -1
    self.close = -1
    self.volume = -1
    self.avg_volume = -1
    self.percent_change = super().initial_float
    self.date = ''
    return
    

# ======================================================= #
#    Price Weekly - Transaction Bridge Table          #
# ======================================================= #

class PW_Transact_Bridge(Base_Model):

  def __init__(self):
    self.row_id = -1
    self.transaction_id = -1
    self.pw_id = -1
    return


# ======================================================= #
#                Price Weekly Table                       #
# ======================================================= #

class Price_Weekly(Base_Model):

  def __init__(self):
    self.weekly_id = -1
    self.open = -1
    self.high = -1
    self.low = -1
    self.close = -1
    self.volume = -1
    self.avg_volume = -1
    self.percent_change = super().initial_float
    self.date = ''
    return
        

# ======================================================= #
#          Price EOD - Price Detail Bridge Table          #
# ======================================================= #

class PEOD_PD_Bridge(Base_Model):

  def __init__(self):
    self.row_id = -1
    self.eod_id = -1
    self.price_detail_id = -1
    return


# ======================================================= #
#                Price per Day (30Min) Table              #
# ======================================================= #

class Price_Detail(Base_Model):

  def __init__(self):
    self.price_detail_id = -1
    self.open = -1
    self.high = -1
    self.low = -1
    self.close = -1
    self.volume = -1
    self.percent_change = super().initial_float
    self.date = ''
    self.time = ''
    return


# ======================================================= #
#              Technical Indicators Table                 #
# ======================================================= #

class Technical_Indicators(Base_Model):

  def __init__(self):
    self.eod_id = -1
    self.atr = super().initial_float
    self.boll_bands = super().initial_float
    self.sma = super().initial_float
    self.ema = super().initial_float
    self.average_directional_movement = super().initial_float
    self.chaikin_osc = super().initial_float
    self.chaikin_a_d_line = super().initial_float
    self.beta = super().initial_float
    self.balance_of_power = super().initial_float
    self.commodity_channel_index = super().initial_float
    self.chande_momentum_oscillator = super().initial_float
    self.pearsons_coefficient = super().initial_float
    self.double_ema = super().initial_float
    self.directional_movement_index = super().initial_float
    self.kaufman_adaptive_ma = super().initial_float
    self.linear_reg = super().initial_float
    self.linear_reg_angle = super().initial_float
    self.linear_reg_intercept = super().initial_float
    self.linear_reg_slope = super().initial_float
    self.macd_conv_diver = super().initial_float
    self.mesa_adaptive_ma = super().initial_float
    self.money_flow_index = super().initial_float
    self.momentum  = super().initial_float
    self.normalized_atr = super().initial_float
    self.obv = super().initial_float
    self.percent_price_osc = super().initial_float
    self.rsi = super().initial_float
    self.parabolic_sar = super().initial_float
    self.parabolic_sar_ext = super().initial_float
    self.std_deviation = super().initial_float
    self.stochastic = super().initial_float
    self.stochastic_fast = super().initial_float
    self.stochastic_rsi = super().initial_float
    self.triple_ema = super().initial_float
    self.true_range = super().initial_float
    self.triangluar_ma = super().initial_float
    self.ultimate_osc = super().initial_float
    self.williams_percent_r = super().initial_float
    self.weighted_ma = super().initial_float
    self.resistance_point = super().initial_float
    self.support_point = super().initial_float
    return


# ======================================================= #
#             Fundmental Statistics Table                 #
# ======================================================= #

class Fundamental_Indicators(Base_Model):

  def __init__(self):
    return


# ======================================================= #
#                Charting Table                           #
# ======================================================= #

# returns float to say -100 is bearish 100 is bullish

class Chart_Indicators(Base_Model):

  def __init__(self):
    self.eod_id = -1
    self.two_crows = super().initial_float
    self.three_black_crows = super().initial_float
    self.three_inside_up_down = super().initial_float
    self.three_outside_up_down = super().initial_float
    self.three_line_strike = super().initial_float
    self.three_stars_south = super().initial_float
    self.three_adv_soliders = super().initial_float
    self.abandoned_baby = super().initial_float
    self.advance_block = super().initial_float
    self.belt_hold = super().initial_float
    self.breakaway = super().initial_float
    self.marubozu_closing = super().initial_float
    self.concealing_baby_swallow = super().initial_float
    self.counterattack = super().initial_float
    self.dark_cloud_cover = super().initial_float
    self.doji = super().initial_float
    self.doji_star = super().initial_float
    self.doji_dragonfly = super().initial_float
    self.engulfing_pattern = super().initial_float
    self.gravestone_doji = super().initial_float
    self.hammer = super().initial_float
    self.hanging_man = super().initial_float
    self.harami_pattern = super().initial_float
    self.harami_cross_pattern = super().initial_float
    self.high_wave_candle = super().initial_float
    self.hikkake_pattern = super().initial_float
    self.hikkake_mod_pattern = super().initial_float
    self.homing_pigeon = super().initial_float
    self.identical_three_crows = super().initial_float
    self.in_neck_pattern = super().initial_float
    self.inverted_hammer = super().initial_float
    self.kicking = super().initial_float
    self.ladder_bottom = super().initial_float
    self.doji_long_leg = super().initial_float
    self.long_line_candle = super().initial_float
    self.marubozu = super().initial_float
    self.matching_low = super().initial_float
    self.mat_hold = super().initial_float
    self.doji_morning_star = super().initial_float
    self.morning_star = super().initial_float
    self.on_neck_pattern = super().initial_float
    self.piercing_pattern = super().initial_float
    self.rickshaw_man = super().initial_float
    self.rise_fall_three_methods = super().initial_float
    self.seperating_lines = super().initial_float
    self.shooting_star = super().initial_float
    self.short_line_candle = super().initial_float
    self.spinning_top = super().initial_float
    self.stalled_pattern = super().initial_float
    self.stick_sandwhich = super().initial_float
    self.doji_tasuki = super().initial_float
    self.tasuki_gap = super().initial_float
    self.thrusting_pattern = super().initial_float
    self.tristar_pattern = super().initial_float
    self.three_unique_river = super().initial_float
    self.three_upside_gap_river = super().initial_float
    return

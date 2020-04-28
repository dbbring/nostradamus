#! /usr/bin/env python
# =================== Gen Imports ===========================
import requests
import time
import json
import numpy as np
from collections import OrderedDict
import talib
import os
import trendln

# ================ Custom Imports ===========================
from shared.base_model import Base_Model
from shared.models import Chart_Indicators, Price_EOD, Price_Weekly, Technical_Indicators, Fundamental_Indicators




# ============================================================ # 
#                   Abstract Class                              #
# ============================================================= #


class API_Request(object):
    
    def __init__(self):
        return

    # Oversimplifed to abstract away a common use case.
    def get_request(self, _url):
        r = requests.get(url=_url)
        return r.json()





 # =========================================================== # 
 #                 AlphaVantage API Calls                       #
 # ============================================================ #

class AlphaVantage(API_Request):

    # @params (ticker, is daily) - ticker - what we are looking for, and either daily or weekly.
    # @descrip - Init by making api call and populating our data dict.
    # @returns dict - either empty dict for failure or data array dict
    def __init__(self, ticker: str, is_daily=True):
        self.base = super()
        self.ticker = ticker
        self.total_lookback_days = 100 # One TA indicator needs to go this far back
        self.api_key = os.environ['AV_API_KEY']
        self.data = self.try_api_call(is_daily)
        try:
            self.data = self.data['Time Series (Daily)'] if is_daily else self.data['Weekly Time Series']
        except KeyError:
            # Let self.data be whatever it is
            pass
        
        return


    # @params (is_daily: bool) - Whether we should get daily or weekly data.
    # @descrip - Try api call, if fails then return empty dict.
    # @returns dict - either empty dict for failure or data array dict
    def try_api_call(self, is_daily=True) -> dict:
        if (is_daily):
            r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + self.ticker + '&apikey=' + self.api_key)
            res = r.json()
        else:
            r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + self.ticker + '&apikey=' + self.api_key)
            res = r.json()
        if 'note' in res:
            return {}
        elif 'error' in res:
            return {}
        return res['Time Series (Daily)'] if is_daily else res['Weekly Time Series']


    # @params (None)
    # @descrip - Blow up data array and seperate into individual arrays of OHLC and reverse because when we do our math, it is seqencal from the begining
    # @returns (dict) - dict of nparray's (OHLC, Vol, Avg Vol)
    def get_inputs(self) -> dict:
        current_period = 0 # count today for calculations but dont save it
        date_data = []
        percent_change_data = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []
        volume_data = []
        inputs = OrderedDict()

        for day in self.data:
            if current_period <= self.total_lookback_days:
                date_data.append(day)
                percent_change_data.append(Base_Model.to_percent(self, float(self.data[day]['1. open']), float(self.data[day]['4. close'])))
                open_data.append(float(self.data[day]['1. open']))
                high_data.append(float(self.data[day]['2. high']))
                low_data.append(float(self.data[day]['3. low']))
                close_data.append(float(self.data[day]['4. close']))
                volume_data.append(float(self.data[day]['5. volume']))
            current_period += 1

        # [::-1] Reverses array 
        inputs['open'] = np.array(open_data[::-1])
        inputs['high'] = np.array(high_data[::-1])
        inputs['low'] = np.array(low_data[::-1])
        inputs['close'] = np.array(close_data[::-1])
        inputs['volume'] = np.array(volume_data[::-1])
        inputs['date'] = date_data[::-1]
        inputs['percent_change'] = percent_change_data[::-1]

        inputs['avg_volume'] = talib.SMA(inputs['volume'], timeperiod=50)

        return inputs


    # @params (inputs, index, istracking) -inputs(dict of NP Arrays), index (which ohlc do we want to piece back toeghther), is tracking (really?)
    # @descrip - Makes a Price_EOD model, and populates with our inputs data
    # @returns (Price_EOD) - a Price_EOD model that is ready for saving
    def make_price_eod_model(self, inputs: dict, index: int, is_tracking=False) -> Price_EOD:
        # Class factory to generate each price eod's 
        eod_model = Price_EOD()

        eod_model.data['date'] = inputs['date'][index]
        eod_model.data['open'] = inputs['open'][index]
        eod_model.data['high'] = inputs['high'][index]
        eod_model.data['low'] = inputs['low'][index]
        eod_model.data['close'] = inputs['close'][index]
        eod_model.data['volume'] = inputs['volume'][index]
        eod_model.data['avg_volume'] = inputs['avg_volume'][index]
        eod_model.data['percent_change'] = inputs['percent_change'][index]
        eod_model.data['is_tracking_period'] = is_tracking

        return eod_model


    # @params (inputs, index) -inputs(dict of NP Arrays), index (which ohlc do we want to piece back toeghther)
    # @descrip - Makes a Price_Weekly model, and populates with our inputs data
    # @returns (Price_Weekly) - a Price_Weekly model that is ready for saving
    def make_price_wk_model(self, inputs: dict, index: int) -> Price_Weekly:
        # Class factory to generate each price weekly 
        try:
            wk_model = Price_Weekly()

            wk_model.data['date'] = inputs['date'][index]
            wk_model.data['open'] = inputs['open'][index]
            wk_model.data['high'] = inputs['high'][index]
            wk_model.data['low'] = inputs['low'][index]
            wk_model.data['close'] = inputs['close'][index]
            wk_model.data['volume'] = inputs['volume'][index]
            wk_model.data['avg_volume'] = inputs['avg_volume'][index]
            wk_model.data['percent_change'] = inputs['percent_change'][index]
            return wk_model
        except Exception:
            # oh well,we may not have 5 weeks worth of data
            # thats ok, but if we dont have 5 days worth data, do blow up because we dont want to anaylze a company less than a week old.
            return None


    # @params (inputs, index) -inputs(dict of NP Arrays), index (which ohlc do we want to piece back toeghther)
    # @descrip - Uses TALIB to populate our Technical Model for each EOD
    # @returns (Technical_Indicators - a Technical_Indicators model that is ready for saving
    def make_tech_indic_model(self, inputs: dict, index: int) -> Technical_Indicators:
        # Class factory to generate each price eod's techincal anaylisis
        ta = Technical_Indicators()

        ta.data['atr_3_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=3)[index]
        ta.data['atr_10_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=10)[index]
        ta.data['atr_15_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=15)[index]
        ta.data['atr_20_period'] = talib.ATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)[index]

        tempBB = talib.BBANDS(inputs['close'], timeperiod=3)

        ta.data['boll_bands_upper_3_period'] = tempBB[0][index]
        ta.data['boll_bands_middle_3_period'] = tempBB[1][index]
        ta.data['boll_bands_lower_3_period'] = tempBB[2][index]

        tempBB = talib.BBANDS(inputs['close'], timeperiod=10)

        ta.data['boll_bands_upper_10_period'] = tempBB[0][index]
        ta.data['boll_bands_middle_10_period'] = tempBB[1][index]
        ta.data['boll_bands_lower_10_period'] = tempBB[2][index]

        tempBB = talib.BBANDS(inputs['close'], timeperiod=15)

        ta.data['boll_bands_upper_15_period'] = tempBB[0][index]
        ta.data['boll_bands_middle_15_period'] = tempBB[1][index]
        ta.data['boll_bands_lower_15_period'] = tempBB[2][index]

        tempBB = talib.BBANDS(inputs['close'], timeperiod=20)

        ta.data['boll_bands_upper_20_period'] = tempBB[0][index]
        ta.data['boll_bands_middle_20_period'] = tempBB[1][index]
        ta.data['boll_bands_lower_20_period'] = tempBB[2][index]

        ta.data['sma_3_period'] = talib.SMA(inputs['close'], timeperiod=3)[index]
        ta.data['sma_10_period'] = talib.SMA(inputs['close'], timeperiod=10)[index]
        ta.data['sma_15_period'] = talib.SMA(inputs['close'], timeperiod=15)[index]
        ta.data['sma_20_period'] = talib.SMA(inputs['close'], timeperiod=20)[index]

        ta.data['ema_3_period'] = talib.EMA(inputs['close'], timeperiod=3)[index]
        ta.data['ema_10_period'] = talib.EMA(inputs['close'], timeperiod=10)[index]
        ta.data['ema_15_period'] = talib.EMA(inputs['close'], timeperiod=15)[index]
        ta.data['ema_20_period'] = talib.EMA(inputs['close'], timeperiod=20)[index]

        ta.data['average_directional_movement_3_period'] = talib.ADX(inputs['high'], inputs['low'], inputs['close'], timeperiod=3)[index]
        ta.data['average_directional_movement_10_period'] = talib.ADX(inputs['high'], inputs['low'], inputs['close'], timeperiod=10)[index]
        ta.data['average_directional_movement_15_period'] = talib.ADX(inputs['high'], inputs['low'], inputs['close'], timeperiod=15)[index]
        ta.data['average_directional_movement_20_period'] = talib.ADX(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)[index]

        ta.data['chaikin_osc_fast_3_slow_10'] = talib.ADOSC(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], fastperiod=3, slowperiod=10)[index]
        ta.data['chaikin_osc_fast_6_slow_18'] = talib.ADOSC(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], fastperiod=6, slowperiod=18)[index]
        ta.data['chaikin_osc_fast_10_slow_20'] = talib.ADOSC(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], fastperiod=10, slowperiod=20)[index]
        ta.data['chaikin_a_d_line'] = talib.AD(inputs['high'], inputs['low'], inputs['close'], inputs['volume'])[index]

        ta.data['balance_of_power'] = talib.BOP(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index]

        ta.data['commodity_channel_index_3_period'] = talib.CCI(inputs['high'], inputs['low'], inputs['close'], timeperiod=3)[index]
        ta.data['commodity_channel_index_10_period'] = talib.CCI(inputs['high'], inputs['low'], inputs['close'], timeperiod=10)[index]
        ta.data['commodity_channel_index_15_period'] = talib.CCI(inputs['high'], inputs['low'], inputs['close'], timeperiod=15)[index]
        ta.data['commodity_channel_index_20_period'] = talib.CCI(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)[index]

        ta.data['chande_momentum_oscillator_3_period'] = talib.CMO(inputs['close'], timeperiod=3)[index]
        ta.data['chande_momentum_oscillator_10_period'] = talib.CMO(inputs['close'], timeperiod=10)[index]
        ta.data['chande_momentum_oscillator_15_period'] = talib.CMO(inputs['close'], timeperiod=15)[index]
        ta.data['chande_momentum_oscillator_20_period'] = talib.CMO(inputs['close'], timeperiod=20)[index]

        ta.data['pearsons_coeff_close_vol_5_period'] = talib.CORREL(inputs['close'], inputs['volume'], timeperiod=5)[index]
        ta.data['pearsons_coeff_close_vol_15_period'] = talib.CORREL(inputs['close'], inputs['volume'], timeperiod=15)[index]
        ta.data['pearsons_coeff_close_vol_30_period'] = talib.CORREL(inputs['close'], inputs['volume'], timeperiod=30)[index]

        ta.data['pearsons_coeff_close_avg_vol_5_period'] = talib.CORREL(inputs['close'], inputs['avg_volume'], timeperiod=5)[index]
        ta.data['pearsons_coeff_close_avg_vol_15_period'] = talib.CORREL(inputs['close'], inputs['avg_volume'], timeperiod=15)[index]
        ta.data['pearsons_coeff_close_avg_vol_30_period'] = talib.CORREL(inputs['close'], inputs['avg_volume'], timeperiod=30)[index]

        ta.data['pearsons_coeff_close_sp_5_period'] = talib.CORREL(inputs['close'], inputs['s_p'], timeperiod=5)[index]
        ta.data['pearsons_coeff_close_sp_15_period'] = talib.CORREL(inputs['close'], inputs['s_p'], timeperiod=15)[index]
        ta.data['pearsons_coeff_close_sp_30_period'] = talib.CORREL(inputs['close'], inputs['s_p'], timeperiod=30)[index]

        ta.data['double_ema_3_period'] = talib.DEMA(inputs['close'], timeperiod=3)[index]
        ta.data['double_ema_10_period'] = talib.DEMA(inputs['close'], timeperiod=10)[index]
        ta.data['double_ema_15_period'] = talib.DEMA(inputs['close'], timeperiod=15)[index]
        ta.data['double_ema_20_period'] = talib.DEMA(inputs['close'], timeperiod=20)[index]

        ta.data['directional_movement_index_3_period'] = talib.DX(inputs['high'], inputs['low'], inputs['close'], timeperiod=3)[index]
        ta.data['directional_movement_index_10_period'] = talib.DX(inputs['high'], inputs['low'], inputs['close'], timeperiod=10)[index]
        ta.data['directional_movement_index_15_period'] = talib.DX(inputs['high'], inputs['low'], inputs['close'], timeperiod=15)[index]
        ta.data['directional_movement_index_20_period'] = talib.DX(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)[index]

        ta.data['kaufman_adaptive_ma_5_period'] = talib.KAMA(inputs['close'], timeperiod=5)[index]
        ta.data['kaufman_adaptive_ma_15_period'] = talib.KAMA(inputs['close'], timeperiod=15)[index]
        ta.data['kaufman_adaptive_ma_30_period'] = talib.KAMA(inputs['close'], timeperiod=30)[index]

        ta.data['linear_reg_3_period'] = talib.LINEARREG(inputs['close'], timeperiod=3)[index]
        ta.data['linear_reg_10_period'] = talib.LINEARREG(inputs['close'], timeperiod=10)[index]
        ta.data['linear_reg_15_period'] = talib.LINEARREG(inputs['close'], timeperiod=15)[index]
        ta.data['linear_reg_20_period'] = talib.LINEARREG(inputs['close'], timeperiod=20)[index]

        ta.data['linear_reg_angle_3_period'] = talib.LINEARREG_ANGLE(inputs['close'], timeperiod=3)[index]
        ta.data['linear_reg_angle_10_period'] = talib.LINEARREG_ANGLE(inputs['close'], timeperiod=10)[index]
        ta.data['linear_reg_angle_15_period'] = talib.LINEARREG_ANGLE(inputs['close'], timeperiod=15)[index]
        ta.data['linear_reg_angle_20_period'] = talib.LINEARREG_ANGLE(inputs['close'], timeperiod=20)[index]

        ta.data['linear_reg_intercept_3_period'] = talib.LINEARREG_INTERCEPT(inputs['close'], timeperiod=3)[index]
        ta.data['linear_reg_intercept_10_period'] = talib.LINEARREG_INTERCEPT(inputs['close'], timeperiod=10)[index]
        ta.data['linear_reg_intercept_15_period'] = talib.LINEARREG_INTERCEPT(inputs['close'], timeperiod=15)[index]
        ta.data['linear_reg_intercept_20_period'] = talib.LINEARREG_INTERCEPT(inputs['close'], timeperiod=20)[index]

        ta.data['linear_reg_slope_3_period'] = talib.LINEARREG_SLOPE(inputs['close'], timeperiod=3)[index]
        ta.data['linear_reg_slope_10_period'] = talib.LINEARREG_SLOPE(inputs['close'], timeperiod=10)[index]
        ta.data['linear_reg_slope_15_period'] = talib.LINEARREG_SLOPE(inputs['close'], timeperiod=15)[index]
        ta.data['linear_reg_slope_20_period'] = talib.LINEARREG_SLOPE(inputs['close'], timeperiod=20)[index]

        tempMACD = talib.MACD(inputs['close'], fastperiod=12, slowperiod=26, signalperiod=9)

        ta.data['macd_fast_12_slow_26_sig_9'] = tempMACD[0][index]
        ta.data['macd_signal_fast_12_slow_26_sig_9'] = tempMACD[1][index]
        ta.data['macd_hist_fast_12_slow_26_sig_9'] = tempMACD[2][index]

        tempMACD = talib.MACD(inputs['close'], fastperiod=6, slowperiod=13, signalperiod=5)

        ta.data['macd_fast_6_slow_13_sig_5'] = tempMACD[0][index]
        ta.data['macd_signal_fast_6_slow_13_sig_5'] = tempMACD[1][index]
        ta.data['macd_hist_fast_6_slow_13_sig_5'] = tempMACD[2][index]

        tempMACD = talib.MACD(inputs['close'], fastperiod=18, slowperiod=39, signalperiod=14)

        ta.data['macd_fast_18_slow_39_sig_14'] = tempMACD[0][index]
        ta.data['macd_signal_fast_18_slow_39_sig_14'] = tempMACD[1][index]
        ta.data['macd_hist_fast_18_slow_39_sig_14'] = tempMACD[2][index]

        tempMAMA = talib.MAMA(inputs['close'])

        ta.data['mesa_adaptive_ma_mama'] = tempMAMA[0][index]
        ta.data['mesa_adaptive_ma_fama'] = tempMAMA[1][index]
        
        ta.data['money_flow_index_3_period'] = talib.MFI(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], timeperiod=3)[index]
        ta.data['money_flow_index_10_period'] = talib.MFI(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], timeperiod=10)[index]
        ta.data['money_flow_index_15_period'] = talib.MFI(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], timeperiod=15)[index]
        ta.data['money_flow_index_20_period'] = talib.MFI(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], timeperiod=20)[index]

        ta.data['momentum_3_period'] = talib.MOM(inputs['close'], timeperiod=3)[index]
        ta.data['momentum_10_period'] = talib.MOM(inputs['close'], timeperiod=10)[index]
        ta.data['momentum_15_period'] = talib.MOM(inputs['close'], timeperiod=15)[index]
        ta.data['momentum_20_period'] = talib.MOM(inputs['close'], timeperiod=20)[index]

        ta.data['normalized_atr_3_period'] = talib.NATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=3)[index]
        ta.data['normalized_atr_10_period'] = talib.NATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=10)[index]
        ta.data['normalized_atr_15_period'] = talib.NATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=15)[index]
        ta.data['normalized_atr_20_period'] = talib.NATR(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)[index]

        ta.data['obv'] = talib.OBV(inputs['close'], inputs['volume'])[index]

        ta.data['percent_price_osc_fast_6_slow_13'] = talib.PPO(inputs['close'], fastperiod=6, slowperiod=13)[index]
        ta.data['percent_price_osc_fast_12_slow_26'] = talib.PPO(inputs['close'], fastperiod=12, slowperiod=26)[index]
        ta.data['percent_price_osc_fast_18_slow_38'] = talib.PPO(inputs['close'], fastperiod=18, slowperiod=38)[index]

        ta.data['rsi_3_period'] = talib.RSI(inputs['close'], timeperiod=3)[index]
        ta.data['rsi_10_period'] = talib.RSI(inputs['close'], timeperiod=10)[index]
        ta.data['rsi_15_period'] = talib.RSI(inputs['close'], timeperiod=15)[index]
        ta.data['rsi_20_period'] = talib.RSI(inputs['close'], timeperiod=20)[index]

        ta.data['parabolic_sar'] = talib.SAR(inputs['high'], inputs['low'])[index]
        ta.data['parabolic_sar_ext'] = talib.SAREXT(inputs['high'], inputs['low'])[index]

        ta.data['std_deviation_3_period'] = talib.STDDEV(inputs['close'], timeperiod=3)[index]
        ta.data['std_deviation_10_period'] = talib.STDDEV(inputs['close'], timeperiod=10)[index]
        ta.data['std_deviation_15_period'] = talib.STDDEV(inputs['close'], timeperiod=15)[index]
        ta.data['std_deviation_20_period'] = talib.STDDEV(inputs['close'], timeperiod=20)[index]

        ta.data['std_deviation_dbl_3_period'] = talib.STDDEV(inputs['close'], timeperiod=3, nbdev=2)[index]
        ta.data['std_deviation_dbl_10_period'] = talib.STDDEV(inputs['close'], timeperiod=10, nbdev=2)[index]
        ta.data['std_deviation_dbl_15_period'] = talib.STDDEV(inputs['close'], timeperiod=15, nbdev=2)[index]
        ta.data['std_deviation_dbl_20_period'] = talib.STDDEV(inputs['close'], timeperiod=20, nbdev=2)[index]

        tempStoch = talib.STOCH(inputs['high'], inputs['low'], inputs['close'], fastk_period=5, slowk_period=3, slowd_period=3)

        ta.data['stochastic_sk_fast_5_slow_k_3_slow_d_3'] = tempStoch[0][index]
        ta.data['stochastic_sd_fast_5_slow_k_3_slow_d_3'] = tempStoch[1][index]

        tempStoch = talib.STOCH(inputs['high'], inputs['low'], inputs['close'], fastk_period=20, slowk_period=7, slowd_period=7)

        ta.data['stochastic_sk_fast_20_slow_k_7_slow_d_7'] = tempStoch[0][index]
        ta.data['stochastic_sd_fast_20_slow_k_7_slow_d_7'] = tempStoch[1][index]

        tempStoch = talib.STOCH(inputs['high'], inputs['low'], inputs['close'], fastk_period=20, slowk_period=14, slowd_period=14)

        ta.data['stochastic_sk_fast_20_slow_k_14_slow_d_14'] = tempStoch[0][index]
        ta.data['stochastic_sd_fast_20_slow_k_14_slow_d_14'] = tempStoch[0][index]

        ta.data['triple_ema_3_period'] = talib.T3(inputs['close'], timeperiod=3)[index]
        ta.data['triple_ema_10_period'] = talib.T3(inputs['close'], timeperiod=10)[index]
        ta.data['triple_ema_15_period'] = talib.T3(inputs['close'], timeperiod=15)[index]

        ta.data['true_range'] = talib.TRANGE(inputs['high'], inputs['low'], inputs['close'])[index]

        ta.data['triangluar_ma_15_period'] = talib.TRIMA(inputs['close'], timeperiod=15)[index]
        ta.data['triangluar_ma_30_period'] = talib.TRIMA(inputs['close'], timeperiod=30)[index]

        ta.data['ultimate_osc_3_6_12_period'] = talib.ULTOSC(inputs['high'], inputs['low'], inputs['close'], timeperiod1=3, timeperiod2=6, timeperiod3=12)[index]
        ta.data['ultimate_osc_7_14_28_period'] = talib.ULTOSC(inputs['high'], inputs['low'], inputs['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)[index]
        ta.data['ultimate_osc_10_20_40_period'] = talib.ULTOSC(inputs['high'], inputs['low'], inputs['close'], timeperiod1=10, timeperiod2=20, timeperiod3=40)[index]

        ta.data['williams_percent_r_3_period'] = talib.WILLR(inputs['high'], inputs['low'], inputs['close'], timeperiod=3)[index]
        ta.data['williams_percent_r_10_period'] = talib.WILLR(inputs['high'], inputs['low'], inputs['close'], timeperiod=10)[index]
        ta.data['williams_percent_r_15_period'] = talib.WILLR(inputs['high'], inputs['low'], inputs['close'], timeperiod=15)[index]
        ta.data['williams_percent_r_20_period'] = talib.WILLR(inputs['high'], inputs['low'], inputs['close'], timeperiod=20)[index]

        ta.data['weighted_ma_3_period'] = talib.WMA(inputs['close'], timeperiod=3)[index]
        ta.data['weighted_ma_10_period'] = talib.WMA(inputs['close'], timeperiod=10)[index]
        ta.data['weighted_ma_15_period'] = talib.WMA(inputs['close'], timeperiod=15)[index]
        ta.data['weighted_ma_20_period'] = talib.WMA(inputs['close'], timeperiod=20)[index]
        
        return ta

    
    # @params (inputs, index) -inputs(dict of NP Arrays), index (which ohlc do we want to piece back toeghther)
    # @descrip - Uses TALIB to populate our Chart Model for each EOD, either -100 for no, 0 for unsure, or 100 for yes.
    # @returns (Chart_Indicators) - a Chart_Indicators model that is ready for saving
    def make_chart_idic_model(self, inputs: dict, index: int) -> Chart_Indicators:
        # Class factory to generate each price eod's chart anaylisis 
        ca = Chart_Indicators()

        ca.data['two_crows'] = int(talib.CDL2CROWS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_black_crows'] = int(talib.CDL3BLACKCROWS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_inside_up_down'] = int(talib.CDL3INSIDE(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_outside_up_down'] = int(talib.CDL3OUTSIDE(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_line_strike'] = int(talib.CDL3LINESTRIKE(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_stars_south'] = int(talib.CDL3STARSINSOUTH(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_adv_soliders'] = int(talib.CDL3WHITESOLDIERS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['abandoned_baby'] = int(talib.CDLABANDONEDBABY(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['advance_block'] = int(talib.CDLADVANCEBLOCK(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['belt_hold'] = int(talib.CDLBELTHOLD(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['breakaway'] = int(talib.CDLBREAKAWAY(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['marubozu_closing'] = int(talib.CDLCLOSINGMARUBOZU(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['concealing_baby_swallow'] = int(talib.CDLCONCEALBABYSWALL(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['counterattack'] = int(talib.CDLCOUNTERATTACK(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['dark_cloud_cover'] = int(talib.CDLDARKCLOUDCOVER(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['doji'] = int(talib.CDLDOJI(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['doji_star'] = int(talib.CDLDOJISTAR(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['doji_dragonfly'] = int(talib.CDLDRAGONFLYDOJI(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['engulfing_pattern'] = int(talib.CDLENGULFING(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['gravestone_doji'] = int(talib.CDLGRAVESTONEDOJI(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['hammer'] = int(talib.CDLHAMMER(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['hanging_man'] = int(talib.CDLHANGINGMAN(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['harami_pattern'] = int(talib.CDLHARAMI(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['harami_cross_pattern'] = int(talib.CDLHARAMICROSS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['high_wave_candle'] = int(talib.CDLHIGHWAVE(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['hikkake_pattern'] = int(talib.CDLHIKKAKE(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['hikkake_mod_pattern'] = int(talib.CDLHIKKAKEMOD(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['homing_pigeon'] = int(talib.CDLHOMINGPIGEON(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['identical_three_crows'] = int(talib.CDLIDENTICAL3CROWS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['in_neck_pattern'] = int(talib.CDLINNECK(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['inverted_hammer'] = int(talib.CDLINVERTEDHAMMER(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['kicking'] = int(talib.CDLKICKING(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['ladder_bottom'] = int(talib.CDLLADDERBOTTOM(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['doji_long_leg'] = int(talib.CDLLONGLEGGEDDOJI(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['long_line_candle'] = int(talib.CDLLONGLINE(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['marubozu'] = int(talib.CDLMARUBOZU(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['matching_low'] = int(talib.CDLMATCHINGLOW(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['mat_hold'] = int(talib.CDLMATHOLD(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['doji_morning_star'] = int(talib.CDLMORNINGDOJISTAR(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['morning_star'] = int(talib.CDLMORNINGSTAR(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['on_neck_pattern'] = int(talib.CDLONNECK(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['piercing_pattern'] = int(talib.CDLPIERCING(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['rickshaw_man'] = int(talib.CDLRICKSHAWMAN(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['rise_fall_three_methods'] = int(talib.CDLRISEFALL3METHODS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['seperating_lines'] = int(talib.CDLSEPARATINGLINES(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['shooting_star'] = int(talib.CDLSHOOTINGSTAR(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['short_line_candle'] = int(talib.CDLSHORTLINE(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['spinning_top'] = int(talib.CDLSPINNINGTOP(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['stalled_pattern'] = int(talib.CDLSTALLEDPATTERN(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['stick_sandwhich'] = int(talib.CDLSTICKSANDWICH(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['doji_tasuki'] = int(talib.CDLTAKURI(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['tasuki_gap'] = int(talib.CDLTASUKIGAP(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['thrusting_pattern'] = int(talib.CDLTHRUSTING(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['tristar_pattern'] = int(talib.CDLTRISTAR(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_unique_river'] = int(talib.CDLUNIQUE3RIVER(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        ca.data['three_upside_gap_river'] = int(talib.CDLXSIDEGAP3METHODS(inputs['open'], inputs['high'], inputs['low'], inputs['close'])[index])

        return ca




 # ============================================================# 
 #                           IEX API Calls                     #
 # ============================================================#


class IEX(API_Request):

    # @params (ticker) - ticker - what we are looking for
    # @descrip - Init by making api call and populating our data dict from IEX endpoints.
    # @returns dict - aka JSON response.
    def __init__(self, ticker: str):
        self.base = super()
        self.ticker = ticker
        self.api_key = os.environ['IEX_API_KEY']
        
        self.data = self.base.get_request('https://sandbox.iexapis.com/stable/stock/' + ticker + '/advanced-stats?token=Tpk_6b5abe0c3d8048fe82f669873de2665f')

        bs = self.base.get_request('https://sandbox.iexapis.com/stable/stock/' + ticker + '/balance-sheet?token=Tpk_6b5abe0c3d8048fe82f669873de2665f')
        if len(bs['balancesheet']) > 0:
            bs = bs['balancesheet'][0]
            self.data = {**bs, **self.data}

        cs = self.base.get_request('https://sandbox.iexapis.com/stable/stock/' + ticker + '/cash-flow?token=Tpk_6b5abe0c3d8048fe82f669873de2665f')
        if len(cs['cashflow']) > 0:
            cs = cs['cashflow'][0]
            self.data = {**cs, **self.data}

        inc = self.base.get_request('https://sandbox.iexapis.com/stable/stock/' + ticker + '/income?token=Tpk_6b5abe0c3d8048fe82f669873de2665f')
        if len(inc['income']) > 0:
            inc = inc['income'][0]
            self.data = {**inc, **self.data}

        return


    # @params (inputs) - inputs(dict of NP.Arrays)
    # @descrip - Use IEX data to make one off model of Fundamental points
    # @returns (Fundamental_Indicators) - a Fundamental model that is ready for saving
    def make_fund_indic_model(self, inputs: dict) -> Fundamental_Indicators:
        # Class factory to generate fundamentals
        fa = Fundamental_Indicators()

        supp_resis = self.get_support_resistance(inputs)

        fa.data['total_revenue'] = float(self.data['totalRevenue']) if self.data['totalRevenue'] else None
        fa.data['cost_of_revenue'] = float(self.data['costOfRevenue']) if self.data['costOfRevenue'] else None
        fa.data['gross_profit'] = float(self.data['grossProfit']) if self.data['grossProfit'] else None
        fa.data['r_and_d'] = float(self.data['researchAndDevelopment']) if self.data['researchAndDevelopment'] else None
        fa.data['selling_gen_and_admin'] = float(self.data['sellingGeneralAndAdmin']) if self.data['sellingGeneralAndAdmin'] else None
        fa.data['operating_expense'] = float(self.data['operatingExpense']) if self.data['operatingExpense'] else None
        fa.data['operating_income'] = float(self.data['operatingIncome']) if self.data['operatingIncome'] else None
        fa.data['other_income_expense_net'] = float(self.data['otherIncomeExpenseNet']) if self.data['otherIncomeExpenseNet'] else None
        fa.data['ebit'] = float(self.data['ebit']) if self.data['ebit'] else None
        fa.data['intrest_income'] = float(self.data['interestIncome']) if self.data['interestIncome'] else None
        fa.data['pretax_income'] = float(self.data['pretaxIncome']) if self.data['pretaxIncome'] else None
        fa.data['income_tax'] = float(self.data['incomeTax']) if self.data['incomeTax'] else None
        fa.data['minority_intrest'] = float(self.data['minorityInterest']) if self.data['minorityInterest'] else None
        fa.data['net_income'] = float(self.data['netIncome']) if self.data['netIncome'] else None
        fa.data['net_income_basic'] = float(self.data['netIncomeBasic']) if self.data['netIncomeBasic'] else None
        fa.data['company_name'] = self.data['companyName']
        fa.data['yr_high'] = float(self.data['week52high']) if self.data['week52high'] else None
        fa.data['yr_low'] = float(self.data['week52low']) if self.data['week52low'] else None
        fa.data['yr_change'] = float(self.data['week52change']) if self.data['week52change'] else None
        fa.data['shares_outstanding'] = float(self.data['sharesOutstanding']) if self.data['sharesOutstanding'] else None
        fa.data['float'] = float(self.data['float']) if self.data['float'] else None
        fa.data['eps_ttm'] = float(self.data['ttmEPS']) if self.data['ttmEPS'] else None
        fa.data['dividend_yield'] = float(self.data['dividendYield']) if self.data['dividendYield'] else None
        fa.data['dividend_rate_ttm'] = float(self.data['ttmDividendRate']) if self.data['ttmDividendRate'] else None
        fa.data['employees'] = float(self.data['employees']) if self.data['employees'] else None
        fa.data['earnings_date'] = self.data['nextEarningsDate']
        fa.data['pe_ratio'] = float(self.data['peRatio']) if self.data['peRatio'] else None
        fa.data['beta'] = float(self.data['beta']) if self.data['beta'] else None
        fa.data['total_cash'] = float(self.data['totalCash']) if self.data['totalCash'] else None
        fa.data['current_debt'] = float(self.data['currentDebt']) if self.data['currentDebt'] else None
        fa.data['ebitda'] = float(self.data['EBITDA']) if self.data['EBITDA'] else None
        fa.data['revenue_per_share'] = float(self.data['revenuePerShare']) if self.data['revenuePerShare'] else None
        fa.data['revenue_per_employee'] = float(self.data['revenuePerEmployee']) if self.data['revenuePerEmployee'] else None
        fa.data['debt_to_equity'] = float(self.data['debtToEquity']) if self.data['debtToEquity'] else None
        fa.data['profit_margin'] = float(self.data['profitMargin']) if self.data['profitMargin'] else None
        fa.data['enterprise_value'] = float(self.data['enterpriseValue']) if self.data['enterpriseValue'] else None
        fa.data['enterprise_value_to_rev'] = float(self.data['enterpriseValueToRevenue']) if self.data['enterpriseValueToRevenue'] else None
        fa.data['price_to_sales'] = float(self.data['priceToSales']) if self.data['priceToSales'] else None
        fa.data['price_to_book'] = float(self.data['priceToBook']) if self.data['priceToBook'] else None
        fa.data['foward_pe_ratio'] = float(self.data['forwardPERatio']) if self.data['forwardPERatio'] else None
        fa.data['peg_ratio'] = float(self.data['pegRatio']) if self.data['pegRatio'] else None
        fa.data['pe_high'] = float(self.data['peHigh']) if self.data['peHigh'] else None
        fa.data['pe_low'] = float(self.data['peLow']) if self.data['peLow'] else None
        fa.data['depreciation'] = float(self.data['depreciation']) if self.data['depreciation'] else None
        fa.data['changes_in_receviables'] = float(self.data['changesInReceivables']) if self.data['changesInReceivables'] else None
        fa.data['changes_in_inventories'] = float(self.data['changesInInventories']) if self.data['changesInInventories'] else None
        fa.data['cash_change'] = float(self.data['cashChange']) if self.data['cashChange'] else None
        fa.data['cash_flow'] = float(self.data['cashFlow']) if self.data['cashFlow'] else None
        fa.data['capital_expenditures'] = float(self.data['capitalExpenditures']) if self.data['capitalExpenditures'] else None
        fa.data['investments'] = float(self.data['investments']) if self.data['investments'] else None
        fa.data['total_investing_cash_flows'] = float(self.data['totalInvestingCashFlows']) if self.data['totalInvestingCashFlows'] else None
        fa.data['dividends_paid'] = float(self.data['dividendsPaid']) if self.data['dividendsPaid'] else None
        fa.data['net_borrowings'] = float(self.data['netBorrowings']) if self.data['netBorrowings'] else None
        fa.data['other_cash_flows'] = float(self.data['otherFinancingCashFlows']) if self.data['otherFinancingCashFlows'] else None
        fa.data['cash_flow_financing'] = float(self.data['cashFlowFinancing']) if self.data['cashFlowFinancing'] else None
        fa.data['balance_sheet_date'] = self.data['reportDate']
        fa.data['current_cash'] = float(self.data['currentCash']) if self.data['currentCash'] else None
        fa.data['short_term_investments'] = float(self.data['shortTermInvestments']) if self.data['shortTermInvestments'] else None
        fa.data['receivables'] = float(self.data['receivables']) if self.data['receivables'] else None
        fa.data['inventory'] = float(self.data['inventory']) if self.data['inventory'] else None
        fa.data['other_current_assets'] = float(self.data['otherCurrentAssets']) if self.data['otherCurrentAssets'] else None
        fa.data['current_assets'] = float(self.data['currentAssets']) if self.data['currentAssets'] else None
        fa.data['long_term_investments'] = float(self.data['longTermInvestments']) if self.data['longTermInvestments'] else None
        fa.data['property_plant_equipment'] = float(self.data['propertyPlantEquipment']) if self.data['propertyPlantEquipment'] else None
        fa.data['goodwill'] = float(self.data['goodwill']) if self.data['goodwill'] else None
        fa.data['intangible_assets'] = float(self.data['intangibleAssets']) if self.data['intangibleAssets'] else None
        fa.data['other_assets'] = float(self.data['otherAssets']) if self.data['otherAssets'] else None
        fa.data['total_assets'] = float(self.data['totalAssets']) if self.data['totalAssets'] else None
        fa.data['accounts_payable'] = float(self.data['accountsPayable']) if self.data['accountsPayable'] else None
        fa.data['current_long_term_debt'] = float(self.data['currentLongTermDebt']) if self.data['currentLongTermDebt'] else None
        fa.data['other_current_liabilites'] = float(self.data['otherCurrentLiabilities']) if self.data['otherCurrentLiabilities'] else None
        fa.data['total_current_liabilites'] = float(self.data['totalCurrentLiabilities']) if self.data['totalCurrentLiabilities'] else None
        fa.data['long_term_debt'] = float(self.data['longTermDebt']) if self.data['longTermDebt'] else None
        fa.data['other_liabilites'] = float(self.data['otherLiabilities']) if self.data['otherLiabilities'] else None
        fa.data['minority_interest'] = float(self.data['minorityInterest']) if self.data['minorityInterest'] else None
        fa.data['total_liabilites'] = float(self.data['totalLiabilities']) if self.data['totalLiabilities'] else None
        fa.data['common_stock'] = float(self.data['commonStock']) if self.data['commonStock'] else None
        fa.data['retained_earnings'] = float(self.data['retainedEarnings']) if self.data['retainedEarnings'] else None
        fa.data['treasury_stock'] = float(self.data['treasuryStock']) if self.data['treasuryStock'] else None
        fa.data['capital_surplus'] = float(self.data['capitalSurplus']) if self.data['capitalSurplus'] else None
        fa.data['shareholder_equity'] = float(self.data['shareholderEquity']) if self.data['shareholderEquity'] else None
        fa.data['net_tangible_assets'] = float(self.data['netTangibleAssets']) if self.data['netTangibleAssets'] else None
        fa.data['avg_30_volume'] = float(self.data['avg30Volume']) if self.data['totalRevenue'] else None
        fa.data['mvg_avg_200'] = float(self.data['day200MovingAvg']) if self.data['totalRevenue'] else None
        fa.data['mvg_avg_50'] = float(self.data['day50MovingAvg']) if self.data['totalRevenue'] else None
        fa.data['max_change_percent'] = float(self.data['maxChangePercent']) if self.data['totalRevenue'] else None
        fa.data['year_5_change_percent'] = float(self.data['year5ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['year_2_change_percent'] = float(self.data['year2ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['year_1_change_percent'] = float(self.data['year1ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['ytd_change_percent'] = float(self.data['ytdChangePercent'])
        fa.data['month_6_change_percent'] = float(self.data['month6ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['month_3_change_percent'] = float(self.data['month3ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['month_1_change_percent'] = float(self.data['month1ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['day_30_change_percent'] = float(self.data['day30ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['day_5_change_percent'] = float(self.data['day5ChangePercent']) if self.data['totalRevenue'] else None
        fa.data['resistance_point_avg'] = supp_resis['avg_resis']
        fa.data['resistance_point'] = supp_resis['resis']
        fa.data['support_point_avg'] = supp_resis['avg_supp']
        fa.data['support_point'] = supp_resis['supp']
        fa.data['book_value'] = fa.data['price_to_book'] * inputs['close'][len(inputs) - 1]

        tempRatio = self.fill_ratios(fa.data['current_assets'], fa.data['current_debt'], fa.data['inventory'], fa.data['total_current_liabilites'], fa.data['total_liabilites'], fa.data['shareholder_equity'], fa.data['long_term_debt'], fa.data['intangible_assets'], fa.data['total_revenue'], fa.data['current_cash'], fa.data['total_assets'], fa.data['book_value'])

        fa.data['quick_ratio'] = tempRatio['quick_ratio']
        fa.data['current_ratio'] = tempRatio['current_ratio']
        fa.data['total_debt_equity_ratio'] = tempRatio['total_debt_equity_ratio']
        fa.data['long_term_debt_equity'] = tempRatio['long_term_debt_equity']
        fa.data['short_term_debt_equity'] = tempRatio['short_term_debt_equity']
        fa.data['intangibles_book_ratio'] = tempRatio['intangibles_book_ratio']
        fa.data['inventory_to_sales_ratio'] = tempRatio['inventory_to_sales_ratio']
        fa.data['long_term_debt_percent_invest_cap'] = tempRatio['long_term_debt_percent_invest_cap']
        fa.data['short_term_debt_percent_invest_cap'] = tempRatio['short_term_debt_percent_invest_cap']
        fa.data['long_term_debt_to_total_debt'] = tempRatio['long_term_debt_to_total_debt']
        fa.data['short_term_debt_to_total_debt'] = tempRatio['short_term_debt_to_total_debt']
        fa.data['total_liabilites_to_total_assets'] = tempRatio['total_liabilites_to_total_assets']
        fa.data['working_capital'] = tempRatio['working_capital']
        
        return fa


    # @params (all) - required data points for calculations
    # @descrip - Checks for None to perform the calculation
    # @returns (dict) - Values are either None or the calcualted value
    def fill_ratios(self, current_assets: float, current_debt: float, inventory: float, total_current_liabilites: float, total_liabilites: float, shareholder_equity: float, long_term_debt: float, intangible_assets: float, total_revenue: float, current_cash: float, total_assets: float, book_value:float ) -> dict:
        data = {
            'quick_ratio': None,
            'current_ratio': None,
            'long_term_debt_equity': None,
            'short_term_debt_equity': None,
            'intangibles_book_ratio': None,
            'inventory_to_sales_ratio': None,
            'total_debt_equity_ratio': None,
            'long_term_debt_percent_invest_cap': None,
            'short_term_debt_percent_invest_cap': None,
            'long_term_debt_to_total_debt': None,
            'short_term_debt_to_total_debt': None,
            'total_liabilites_to_total_assets': None,
            'working_capital': None,
        }
        
        if current_assets and total_current_liabilites and inventory:
            data['quick_ratio'] = (current_assets - inventory) / total_current_liabilites

            data['current_ratio'] = current_assets / total_current_liabilites

        if long_term_debt and shareholder_equity and current_debt:
            data['long_term_debt_equity'] = long_term_debt / shareholder_equity

            data['short_term_debt_equity'] = current_debt / shareholder_equity

        if intangible_assets and book_value:
            data['intangibles_book_ratio'] = intangible_assets / book_value

        if inventory and total_revenue:
            data['inventory_to_sales_ratio'] = inventory / total_revenue

        if total_liabilites and shareholder_equity and total_current_liabilites and current_cash and long_term_debt and total_assets:
            data['total_debt_equity_ratio'] = total_liabilites / shareholder_equity

            data['long_term_debt_percent_invest_cap'] = long_term_debt / (
                shareholder_equity + total_liabilites - total_current_liabilites - current_cash
            )
            data['short_term_debt_percent_invest_cap'] = total_current_liabilites / (
                shareholder_equity + total_liabilites - total_current_liabilites - current_cash
            )
            data['long_term_debt_to_total_debt'] = long_term_debt / total_liabilites

            data['short_term_debt_to_total_debt'] = total_current_liabilites / total_liabilites

            data['total_liabilites_to_total_assets'] = total_liabilites / total_assets

            data['working_capital'] = total_assets - total_liabilites

        return data


    # @params (inputs) - dict of Np.Arrays
    # @descrip - Finds low/highest point of close. Then iterates over each value and keeps count of all other values within a % range and returns value with most common data points.
    # @returns (dict) - Values are either the initial value or the calcuated value.
    def get_support_resistance(self, inputs:dict) -> dict:
        sp_res = OrderedDict()
        min_indexes, max_indexes = trendln.get_extrema(inputs['close'])
        # Initailize at first position
        sp_res['avg_supp'] = inputs['close'][min_indexes[0]]
        sp_res['supp'] = inputs['close'][min_indexes[0]]
        sp_res['avg_resis'] =  inputs['close'][max_indexes[0]]
        sp_res['resis'] =  inputs['close'][max_indexes[0]]
        # Keep running tabs on which closing price has the most similiar closing prices
        temp_counter = OrderedDict()
        temp_counter['avg_min_index'] = {
            'count': 0,
            'index': 0
        }
        temp_counter['avg_max_index'] = {
            'count': 0,
            'index': 0
        }

        for min_index in min_indexes:
            # if our new close price is lower than the previous set it
            sp_res['supp'] = inputs['close'][min_index] if sp_res['supp'] > inputs['close'][min_index] else sp_res['supp']

            tempList = []

            for close in inputs['close']:
                # give 3% window, if the close price is in the range, add it
                if close - (close * 0.03) <= inputs['close'][min_index] <= close + (close * 0.03):
                    tempList.append(close)

            if len(tempList) > temp_counter['avg_min_index']['count']:
               temp_counter['avg_min_index']['count'] = len(tempList)
               temp_counter['avg_min_index']['index'] = min_index

        for max_index in max_indexes:
            sp_res['resis'] = inputs['close'][max_index] if sp_res['resis'] < inputs['close'][max_index] else sp_res['resis']

            tempList = []

            for close in inputs['close']:
                if close - (close * 0.03) <= inputs['close'][max_index] <= close + (close * 0.03):
                    tempList.append(close)

            if len(tempList) > temp_counter['avg_max_index']['count']:
               temp_counter['avg_max_index']['count'] = len(tempList)
               temp_counter['avg_max_index']['index'] = max_index

        return sp_res
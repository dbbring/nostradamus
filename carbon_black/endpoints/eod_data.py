from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Price_EOD, Chart_Indicators, Technical_Indicators
from datetime import datetime


class EOD(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        self.api_endpoint = None
        return

    def get(self, api_endpoint: str, transaction_id: int, include_anaylsis=None) -> dict:
        try:
            self.api_endpoint = api_endpoint
            results = self.query(
                api_endpoint, f"SELECT * FROM Price_EOD WHERE transaction_id = {transaction_id};")
            if include_anaylsis:
                return self.make_eod_model(results, True)
            else:
                return self.make_eod_model(results)
        except Exception as err:
            return {
                'error': {
                    'eod_data': str(repr(err))
                }
            }

    def make_eod_model(self, sql_results: list, include_anaysis=False):
        all_results = []

        for item in sql_results:
            model = Price_EOD()
            model.data['eod_id'] = item[0]
            model.data['transaction_id'] = item[1]
            model.data['date'] = item[2].strftime(
                '%Y-%m-%d') if item[2] else None
            model.data['open'] = item[3]
            model.data['high'] = item[4]
            model.data['low'] = item[5]
            model.data['close'] = item[6]
            model.data['volume'] = item[7]
            model.data['percent_change'] = item[8]
            model.data['is_tracking_period'] = bool(item[9])
            model.data['avg_volume'] = item[10]

            if include_anaysis == 'ca':
                _chart = Charting()
                _ca = _chart.get(self.api_endpoint, item[0])
                model.data['charting'] = _ca[0] if len(_ca) == 1 else _ca

            elif include_anaysis == 'ta':
                _technical = Technical()
                _ta = _technical.get(self.api_endpoint, item[0])
                model.data['technical'] = _ta[0] if len(_ta) == 1 else _ta
            else:
                _chart = Charting()
                _ca = _chart.get(self.api_endpoint, item[0])
                model.data['charting'] = _ca[0] if len(_ca) == 1 else _ca

                _technical = Technical()
                _ta = _technical.get(self.api_endpoint, item[0])
                model.data['technical'] = _ta[0] if len(_ta) == 1 else _ta

            all_results.append(model.data)

        return all_results


class Charting(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        return

    def get(self, api_endpoint: str, eod_id: int) -> dict:
        try:
            results = self.query(
                api_endpoint, f"SELECT * FROM Chart_Indicators WHERE eod_id = {eod_id};")
            return self.make_chart_model(results)
        except Exception as err:
            return {
                'error': {
                    'charting': str(repr(err))
                }
            }

    def make_chart_model(self, sql_results: list):
        all_results = []

        for item in sql_results:
            model = Chart_Indicators()
            model.data['eod_id'] = item[0]
            model.data['two_crows'] = item[1]
            model.data['three_black_crows'] = item[2]
            model.data['three_inside_up_down'] = item[3]
            model.data['three_outside_up_down'] = item[4]
            model.data['three_line_strike'] = item[5]
            model.data['three_stars_south'] = item[6]
            model.data['three_adv_soliders'] = item[7]
            model.data['abandoned_baby'] = item[8]
            model.data['advance_block'] = item[9]
            model.data['belt_hold'] = item[10]
            model.data['breakaway'] = item[11]
            model.data['marubozu_closing'] = item[12]
            model.data['concealing_baby_swallow'] = item[13]
            model.data['counterattack'] = item[14]
            model.data['dark_cloud_cover'] = item[15]
            model.data['doji'] = item[16]
            model.data['doji_star'] = item[17]
            model.data['doji_dragonfly'] = item[18]
            model.data['engulfing_pattern'] = item[19]
            model.data['gravestone_doji'] = item[20]
            model.data['hammer'] = item[21]
            model.data['hanging_man'] = item[22]
            model.data['harami_pattern'] = item[23]
            model.data['harami_cross_pattern'] = item[24]
            model.data['high_wave_candle'] = item[25]
            model.data['hikkake_pattern'] = item[26]
            model.data['hikkake_mod_pattern'] = item[27]
            model.data['homing_pigeon'] = item[28]
            model.data['identical_three_crows'] = item[29]
            model.data['in_neck_pattern'] = item[30]
            model.data['inverted_hammer'] = item[31]
            model.data['kicking'] = item[32]
            model.data['ladder_bottom'] = item[33]
            model.data['doji_long_leg'] = item[34]
            model.data['long_line_candle'] = item[35]
            model.data['marubozu'] = item[36]
            model.data['matching_low'] = item[37]
            model.data['mat_hold'] = item[38]
            model.data['doji_morning_star'] = item[39]
            model.data['morning_star'] = item[40]
            model.data['on_neck_pattern'] = item[41]
            model.data['piercing_pattern'] = item[42]
            model.data['rickshaw_man'] = item[43]
            model.data['rise_fall_three_methods'] = item[44]
            model.data['seperating_lines'] = item[45]
            model.data['shooting_star'] = item[46]
            model.data['short_line_candle'] = item[47]
            model.data['spinning_top'] = item[48]
            model.data['stalled_pattern'] = item[49]
            model.data['stick_sandwhich'] = item[50]
            model.data['doji_tasuki'] = item[51]
            model.data['tasuki_gap'] = item[52]
            model.data['thrusting_pattern'] = item[53]
            model.data['tristar_pattern'] = item[54]
            model.data['three_unique_river'] = item[55]
            model.data['three_upside_gap_river'] = item[56]

            all_results.append(model.data)

        return all_results


class Technical(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        return

    def get(self, api_endpoint: str, eod_id: int) -> dict:
        try:
            results = self.query(
                api_endpoint, f"SELECT * FROM Technical_Indicators WHERE eod_id = {eod_id};")
            return self.make_technical_model(results)
        except Exception as err:
            return {
                'error': {
                    'technical': str(repr(err))
                }
            }

    def make_technical_model(self, sql_results: list):
        all_results = []

        for item in sql_results:
            model = Technical_Indicators()
            model.data['eod_id'] = item[0]
            model.data['atr_3_period'] = item[1]
            model.data['atr_10_period'] = item[2]
            model.data['atr_15_period'] = item[3]
            model.data['atr_20_period'] = item[4]
            model.data['boll_bands_upper_3_period'] = item[5]
            model.data['boll_bands_middle_3_period'] = item[6]
            model.data['boll_bands_lower_3_period'] = item[7]
            model.data['boll_bands_upper_10_period'] = item[8]
            model.data['boll_bands_middle_10_period'] = item[9]
            model.data['boll_bands_lower_10_period'] = item[10]
            model.data['boll_bands_upper_15_period'] = item[11]
            model.data['boll_bands_middle_15_period'] = item[12]
            model.data['boll_bands_lower_15_period'] = item[13]
            model.data['boll_bands_upper_20_period'] = item[14]
            model.data['boll_bands_middle_20_period'] = item[15]
            model.data['boll_bands_lower_20_period'] = item[16]
            model.data['sma_3_period'] = item[17]
            model.data['sma_10_period'] = item[18]
            model.data['sma_15_period'] = item[19]
            model.data['sma_20_period'] = item[20]
            model.data['ema_3_period'] = item[21]
            model.data['ema_10_period'] = item[22]
            model.data['ema_15_period'] = item[23]
            model.data['ema_20_period'] = item[24]
            model.data['average_directional_movement_3_period'] = item[25]
            model.data['average_directional_movement_10_period'] = item[26]
            model.data['average_directional_movement_15_period'] = item[27]
            model.data['average_directional_movement_20_period'] = item[28]
            model.data['chaikin_osc_fast_3_slow_10'] = item[29]
            model.data['chaikin_osc_fast_6_slow_18'] = item[30]
            model.data['chaikin_osc_fast_10_slow_20'] = item[31]
            model.data['chaikin_a_d_line'] = item[32]
            model.data['balance_of_power'] = item[33]
            model.data['commodity_channel_index_3_period'] = item[34]
            model.data['commodity_channel_index_10_period'] = item[35]
            model.data['commodity_channel_index_15_period'] = item[36]
            model.data['commodity_channel_index_20_period'] = item[37]
            model.data['chande_momentum_oscillator_3_period'] = item[38]
            model.data['chande_momentum_oscillator_10_period'] = item[39]
            model.data['chande_momentum_oscillator_15_period'] = item[40]
            model.data['chande_momentum_oscillator_20_period'] = item[41]
            model.data['pearsons_coeff_close_vol_5_period'] = item[42]
            model.data['pearsons_coeff_close_vol_15_period'] = item[43]
            model.data['pearsons_coeff_close_vol_30_period'] = item[44]
            model.data['pearsons_coeff_close_avg_vol_5_period'] = item[45]
            model.data['pearsons_coeff_close_avg_vol_15_period'] = item[46]
            model.data['pearsons_coeff_close_avg_vol_30_period'] = item[47]
            model.data['pearsons_coeff_close_spy_5_period'] = item[48]
            model.data['pearsons_coeff_close_spy_15_period'] = item[49]
            model.data['pearsons_coeff_close_spy_30_period'] = item[50]
            model.data['double_ema_3_period'] = item[51]
            model.data['double_ema_10_period'] = item[52]
            model.data['double_ema_15_period'] = item[53]
            model.data['double_ema_20_period'] = item[54]
            model.data['directional_movement_index_3_period'] = item[55]
            model.data['directional_movement_index_10_period'] = item[56]
            model.data['directional_movement_index_15_period'] = item[57]
            model.data['directional_movement_index_20_period'] = item[58]
            model.data['kaufman_adaptive_ma_5_period'] = item[59]
            model.data['kaufman_adaptive_ma_15_period'] = item[60]
            model.data['kaufman_adaptive_ma_30_period'] = item[61]
            model.data['linear_reg_3_period'] = item[62]
            model.data['linear_reg_10_period'] = item[63]
            model.data['linear_reg_15_period'] = item[64]
            model.data['linear_reg_20_period'] = item[65]
            model.data['linear_reg_angle_3_period'] = item[66]
            model.data['linear_reg_angle_10_period'] = item[67]
            model.data['linear_reg_angle_15_period'] = item[68]
            model.data['linear_reg_angle_20_period'] = item[69]
            model.data['linear_reg_intercept_3_period'] = item[70]
            model.data['linear_reg_intercept_10_period'] = item[71]
            model.data['linear_reg_intercept_15_period'] = item[72]
            model.data['linear_reg_intercept_20_period'] = item[73]
            model.data['linear_reg_slope_3_period'] = item[74]
            model.data['linear_reg_slope_10_period'] = item[75]
            model.data['linear_reg_slope_15_period'] = item[76]
            model.data['linear_reg_slope_20_period'] = item[77]
            model.data['macd_fast_12_slow_26_sig_9'] = item[78]
            model.data['macd_signal_fast_12_slow_26_sig_9'] = item[79]
            model.data['macd_hist_fast_12_slow_26_sig_9'] = item[80]
            model.data['macd_fast_6_slow_13_sig_5'] = item[81]
            model.data['macd_signal_fast_6_slow_13_sig_5'] = item[82]
            model.data['macd_hist_fast_6_slow_13_sig_5'] = item[83]
            model.data['macd_fast_18_slow_39_sig_14'] = item[84]
            model.data['macd_signal_fast_18_slow_39_sig_14'] = item[85]
            model.data['macd_hist_fast_18_slow_39_sig_14'] = item[86]
            model.data['mesa_adaptive_ma_mama'] = item[87]
            model.data['mesa_adaptive_ma_fama'] = item[88]
            model.data['money_flow_index_3_period'] = item[89]
            model.data['money_flow_index_10_period'] = item[90]
            model.data['money_flow_index_15_period'] = item[91]
            model.data['money_flow_index_20_period'] = item[92]
            model.data['momentum_3_period'] = item[93]
            model.data['momentum_10_period'] = item[94]
            model.data['momentum_15_period'] = item[95]
            model.data['momentum_20_period'] = item[96]
            model.data['normalized_atr_3_period'] = item[97]
            model.data['normalized_atr_10_period'] = item[98]
            model.data['normalized_atr_15_period'] = item[99]
            model.data['normalized_atr_20_period'] = item[100]
            model.data['obv'] = item[101]
            model.data['percent_price_osc_fast_6_slow_13'] = item[102]
            model.data['percent_price_osc_fast_12_slow_26'] = item[103]
            model.data['percent_price_osc_fast_18_slow_38'] = item[104]
            model.data['rsi_3_period'] = item[105]
            model.data['rsi_10_period'] = item[106]
            model.data['rsi_15_period'] = item[107]
            model.data['rsi_20_period'] = item[108]
            model.data['parabolic_sar'] = item[109]
            model.data['parabolic_sar_ext'] = item[110]
            model.data['std_deviation_3_period'] = item[111]
            model.data['std_deviation_10_period'] = item[112]
            model.data['std_deviation_15_period'] = item[113]
            model.data['std_deviation_20_period'] = item[114]
            model.data['std_deviation_dbl_3_period'] = item[115]
            model.data['std_deviation_dbl_10_period'] = item[116]
            model.data['std_deviation_dbl_15_period'] = item[117]
            model.data['std_deviation_dbl_20_period'] = item[118]
            model.data['stochastic_sk_fast_5_slow_k_3_slow_d_3'] = item[119]
            model.data['stochastic_sd_fast_5_slow_k_3_slow_d_3'] = item[120]
            model.data['stochastic_sk_fast_20_slow_k_7_slow_d_7'] = item[121]
            model.data['stochastic_sd_fast_20_slow_k_7_slow_d_7'] = item[122]
            model.data['stochastic_sk_fast_20_slow_k_14_slow_d_14'] = item[123]
            model.data['stochastic_sd_fast_20_slow_k_14_slow_d_14'] = item[124]
            model.data['triple_ema_3_period'] = item[125]
            model.data['triple_ema_10_period'] = item[126]
            model.data['triple_ema_15_period'] = item[127]
            model.data['true_range'] = item[128]
            model.data['triangluar_ma_15_period'] = item[129]
            model.data['triangluar_ma_30_period'] = item[130]
            model.data['ultimate_osc_3_6_12_period'] = item[131]
            model.data['ultimate_osc_7_14_28_period'] = item[132]
            model.data['ultimate_osc_10_20_40_period'] = item[133]
            model.data['williams_percent_r_3_period'] = item[134]
            model.data['williams_percent_r_10_period'] = item[135]
            model.data['williams_percent_r_15_period'] = item[136]
            model.data['williams_percent_r_20_period'] = item[137]
            model.data['weighted_ma_3_period'] = item[138]
            model.data['weighted_ma_10_period'] = item[139]
            model.data['weighted_ma_15_period'] = item[140]
            model.data['weighted_ma_20_period'] = item[141]

            all_results.append(model.data)

        return all_results

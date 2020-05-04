from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Fundamental_Indicators
from datetime import datetime


class Fundamental(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        return

    def get(self, api_endpoint: str, transaction_id: int) -> dict:
        try:
            results = super().query(api_endpoint,
                                    f"SELECT * FROM Fundamental_Indicators WHERE transaction_id = {transaction_id};")
            return self.make_fundamental_model(results)
        except Exception as err:
            return {
                'error': str(repr(err))
            }

    def make_fundamental_model(self, sql_results: list):
        all_results = []

        for item in sql_results:
            model = Fundamental_Indicators()
            model.data['transaction_id'] = item[0]
            model.data['total_revenue'] = float(item[1]) if item[1] else None
            model.data['cost_of_revenue'] = float(item[2]) if item[2] else None
            model.data['gross_profit'] = float(item[3]) if item[3] else None
            model.data['r_and_d'] = float(item[4]) if item[4] else None
            model.data['selling_gen_and_admin'] = float(
                item[5]) if item[5] else None
            model.data['operating_expense'] = float(
                item[6]) if item[6] else None
            model.data['operating_income'] = float(
                item[7]) if item[7] else None
            model.data['other_income_expense_net'] = float(
                item[8]) if item[8] else None
            model.data['ebit'] = float(item[9]) if item[9] else None
            model.data['intrest_income'] = float(
                item[10]) if item[10] else None
            model.data['pretax_income'] = float(item[11]) if item[11] else None
            model.data['income_tax'] = float(item[12]) if item[12] else None
            model.data['minority_intrest'] = float(
                item[13]) if item[13] else None
            model.data['net_income'] = float(item[14]) if item[14] else None
            model.data['net_income_basic'] = float(
                item[15]) if item[15] else None
            model.data['company_name'] = item[16]
            model.data['yr_high'] = float(item[17]) if item[17] else None
            model.data['yr_low'] = float(item[18]) if item[18] else None
            model.data['yr_change'] = float(
                item[19] * 100) if item[19] else None
            model.data['shares_outstanding'] = float(
                item[20]) if item[20] else None
            model.data['float'] = float(item[21]) if item[21] else None
            model.data['eps_ttm'] = float(item[22]) if item[22] else None
            model.data['dividend_yield'] = float(
                item[23]) if item[23] else None
            model.data['dividend_rate_ttm'] = float(
                item[24]) if item[24] else None
            model.data['employees'] = float(item[25]) if item[25] else None
            model.data['earnings_date'] = item[26].strftime('%Y-%m-%d')
            model.data['pe_ratio'] = float(item[27]) if item[27] else None
            model.data['beta'] = float(item[28]) if item[28] else None
            model.data['total_cash'] = float(item[29]) if item[29] else None
            model.data['current_debt'] = float(item[30]) if item[30] else None
            model.data['ebitda'] = float(item[31]) if item[31] else None
            model.data['revenue_per_share'] = float(
                item[32]) if item[32] else None
            model.data['revenue_per_employee'] = float(
                item[33]) if item[33] else None
            model.data['debt_to_equity'] = float(
                item[34]) if item[34] else None
            model.data['profit_margin'] = float(item[35]) if item[35] else None
            model.data['enterprise_value'] = float(
                item[36]) if item[36] else None
            model.data['enterprise_value_to_rev'] = float(
                item[37]) if item[37] else None
            model.data['price_to_sales'] = float(
                item[38]) if item[38] else None
            model.data['price_to_book'] = float(item[39]) if item[39] else None
            model.data['foward_pe_ratio'] = float(
                item[40]) if item[40] else None
            model.data['peg_ratio'] = float(item[41]) if item[41] else None
            model.data['pe_high'] = float(item[42]) if item[42] else None
            model.data['pe_low'] = float(item[43]) if item[43] else None
            model.data['depreciation'] = float(item[44]) if item[44] else None
            model.data['changes_in_receviables'] = float(
                item[45]) if item[45] else None
            model.data['changes_in_inventories'] = float(
                item[46]) if item[46] else None
            model.data['cash_change'] = float(item[47]) if item[47] else None
            model.data['cash_flow'] = float(item[48]) if item[48] else None
            model.data['capital_expenditures'] = float(
                item[49]) if item[49] else None
            model.data['investments'] = float(item[50]) if item[50] else None
            model.data['total_investing_cash_flows'] = float(
                item[51]) if item[51] else None
            model.data['dividends_paid'] = float(
                item[52]) if item[52] else None
            model.data['net_borrowings'] = float(
                item[53]) if item[53] else None
            model.data['other_cash_flows'] = float(
                item[54]) if item[54] else None
            model.data['cash_flow_financing'] = float(
                item[55]) if item[55] else None
            model.data['balance_sheet_date'] = item[56].strftime('%Y-%m-%d')
            model.data['current_cash'] = float(item[57]) if item[57] else None
            model.data['short_term_investments'] = float(
                item[58]) if item[58] else None
            model.data['receivables'] = float(item[59]) if item[59] else None
            model.data['inventory'] = float(item[60]) if item[60] else None
            model.data['other_current_assets'] = float(
                item[61]) if item[61] else None
            model.data['current_assets'] = float(
                item[62]) if item[62] else None
            model.data['long_term_investments'] = float(
                item[63]) if item[63] else None
            model.data['property_plant_equipment'] = float(
                item[64]) if item[64] else None
            model.data['goodwill'] = float(item[65]) if item[65] else None
            model.data['intangible_assets'] = float(
                item[66]) if item[66] else None
            model.data['other_assets'] = float(item[67]) if item[67] else None
            model.data['total_assets'] = float(item[68]) if item[68] else None
            model.data['accounts_payable'] = float(
                item[69]) if item[69] else None
            model.data['current_long_term_debt'] = float(
                item[70]) if item[70] else None
            model.data['other_current_liabilites'] = float(
                item[71]) if item[71] else None
            model.data['total_current_liabilites'] = float(
                item[72]) if item[72] else None
            model.data['long_term_debt'] = float(
                item[73]) if item[73] else None
            model.data['other_liabilites'] = float(
                item[74]) if item[74] else None
            model.data['minority_interest'] = float(
                item[75]) if item[75] else None
            model.data['total_liabilites'] = float(
                item[76]) if item[76] else None
            model.data['common_stock'] = float(item[77]) if item[77] else None
            model.data['retained_earnings'] = float(
                item[78]) if item[78] else None
            model.data['treasury_stock'] = float(
                item[79]) if item[79] else None
            model.data['capital_surplus'] = float(
                item[80]) if item[80] else None
            model.data['shareholder_equity'] = float(
                item[81]) if item[81] else None
            model.data['net_tangible_assets'] = float(
                item[82]) if item[82] else None
            model.data['quick_ratio'] = float(item[83]) if item[83] else None
            model.data['current_ratio'] = float(item[84]) if item[84] else None
            model.data['total_debt_equity_ratio'] = float(
                item[85]) if item[85] else None
            model.data['long_term_debt_equity'] = float(
                item[86]) if item[86] else None
            model.data['short_term_debt_equity'] = float(
                item[87]) if item[87] else None
            model.data['intangibles_book_ratio'] = float(
                item[88]) if item[88] else None
            model.data['inventory_to_sales_ratio'] = float(
                item[89]) if item[89] else None
            model.data['long_term_debt_percent_invest_cap'] = float(
                item[90]) if item[90] else None
            model.data['short_term_debt_percent_invest_cap'] = float(
                item[91]) if item[91] else None
            model.data['long_term_debt_to_total_debt'] = float(
                item[92]) if item[92] else None
            model.data['short_term_debt_to_total_debt'] = float(
                item[93]) if item[93] else None
            model.data['total_liabilites_to_total_assets'] = float(
                item[94]) if item[94] else None
            model.data['working_capital'] = float(
                item[95]) if item[95] else None
            model.data['sector'] = item[96]
            model.data['sub_sector'] = item[97]
            model.data['institutional_ownership'] = float(
                item[98]) if item[98] else None
            model.data['short_interest_percent'] = float(
                item[99]) if item[99] else None
            model.data['avg_30_volume'] = float(
                item[100]) if item[100] else None
            model.data['mvg_avg_200'] = float(item[101]) if item[101] else None
            model.data['mvg_avg_50'] = float(item[102]) if item[102] else None
            model.data['max_change_percent'] = float(
                item[103] * 100) if item[103] else None
            model.data['year_5_change_percent'] = float(
                item[104] * 100) if item[104] else None
            model.data['year_2_change_percent'] = float(
                item[105] * 100) if item[105] else None
            model.data['year_1_change_percent'] = float(
                item[106] * 100) if item[106] else None
            model.data['ytd_change_percent'] = float(
                item[107] * 100) if item[107] else None
            model.data['month_6_change_percent'] = float(
                item[108] * 100) if item[108] else None
            model.data['month_3_change_percent'] = float(
                item[109] * 100) if item[109] else None
            model.data['month_1_change_percent'] = float(
                item[110] * 100) if item[110] else None
            model.data['day_30_change_percent'] = float(
                item[111] * 100) if item[111] else None
            model.data['day_5_change_percent'] = float(
                item[112] * 100) if item[112] else None
            model.data['resistance_point_avg'] = float(
                item[113]) if item[113] else None
            model.data['resistance_point'] = float(
                item[114]) if item[114] else None
            model.data['support_point_avg'] = float(
                item[115]) if item[115] else None
            model.data['support_point'] = float(
                item[116]) if item[116] else None
            model.data['book_value'] = float(item[117]) if item[117] else None

            all_results.append(model.data)

        return all_results

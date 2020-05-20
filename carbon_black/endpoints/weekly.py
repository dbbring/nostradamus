from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import Price_Weekly
from datetime import datetime


class Weekly(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        return

    def get(self, api_endpoint: str, transaction_id: int) -> dict:
        try:
            results = self.query(
                api_endpoint, f"SELECT * FROM Price_Weekly WHERE transaction_id = {transaction_id};")
            return self.make_weekly_model(results)
        except Exception as err:
            return {
                'error': {
                    'weekly': str(repr(err))
                }
            }

    def make_weekly_model(self, sql_results: list):
        all_results = []

        for item in sql_results:
            model = Price_Weekly()
            model.data['weekly_id'] = item[0]
            model.data['transaction_id'] = item[1]
            model.data['date'] = item[2].strftime(
                '%Y-%m-%d') if item[2] else None
            model.data['open'] = item[3]
            model.data['high'] = item[4]
            model.data['low'] = item[5]
            model.data['close'] = item[6]
            model.data['volume'] = item[7]
            model.data['avg_volume'] = item[8]
            model.data['percent_change'] = item[9]
            model.data['price_diff_open_to_low'] = model.to_percent(
                item[3], item[5])
            model.data['vol_diff_from_avg'] = model.to_percent(
                item[8], item[7])

            all_results.append(model.data)

        return all_results

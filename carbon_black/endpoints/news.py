from carbon_black.endpoints.base_endpoint import Endpoint
from shared.models import News_Event
from datetime import datetime


class News(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        return

    def get(self, api_endpoint: str, transaction_id: int) -> dict:
        try:
            results = super().query(api_endpoint,
                                    f"SELECT * FROM News_Event WHERE transaction_id = {transaction_id};")
            return self.make_news_model(results)
        except Exception as err:
            return {
                'error': str(repr(err))
            }

    def make_news_model(self, sql_results: list):
        all_results = []

        for item in sql_results:
            model = News_Event()
            model.data['news_event_id'] = item[0]
            model.data['transaction_id'] = item[1]
            model.data['date_of_article'] = item[2].strftime('%Y-%m-%d')
            model.data['title_of_article'] = item[3]
            model.data['link'] = item[4]
            model.data['source'] = item[5]

            all_results.append(model.data)

        return all_results

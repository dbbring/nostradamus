from carbon_black.endpoints.base_endpoint import Endpoint


class Stats(Endpoint):

    def __init__(self) -> None:
        super().__init__()
        return

    def get(self) -> dict:
        all_results = []

        for data_item in self.config['nostradamus']:
            db_result = self.query(
                data_item['api_endpoint'], "SELECT COUNT(transaction_id) FROM Transaction;")

            db_dups = self.query(
                data_item['api_endpoint'], "SELECT ticker, COUNT(ticker) AS dups FROM Transaction GROUP BY ticker HAVING (dups > 1);")

            dups = []
            for dup_item in db_dups:
                dups.append({
                    'ticker': dup_item[0],
                    'count': dup_item[1]
                })

            all_results.append({
                'api_endpoint': data_item['api_endpoint'],
                'total_items': db_result[0][0],
                'duplicate_items': dups
            })

        return all_results[0] if all_results == 1 else all_results

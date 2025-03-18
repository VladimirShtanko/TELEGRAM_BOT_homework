import requests
import json
from config import keys


class APIException(Exception):
    pass

class CriptoConvertor:
    @staticmethod
    def convert (quote: str, base: str, amount: str ):

        if quote == base:
            raise APIException('Значения не могут быть равны ')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать вылюту{quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать вылюту{base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        url = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        total_base = json.loads(url.content)[keys[base]]

        return total_base


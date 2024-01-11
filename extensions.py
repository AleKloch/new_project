
import requests
import json
from config import headers



class APIException(Exception):
    pass
class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        else:
            response = requests.request("GET", f"https://api.apilayer.com/currency_data/convert?to={quote}&from={base}&amount={amount}", headers=headers, data="")
            result = json.loads(response.content)
            price = result['result']
            round_price = round(price, 1)
            return round_price

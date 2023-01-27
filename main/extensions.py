import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def converter(quote, base, amount=None):
        if quote == base:
            raise ConversionException(f"Нельзя конвертировать ту же валюту {quote}!")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {quote}!")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {base}!")

        if amount:
            try:
                amount = float(amount)
            except ValueError:
                raise ConversionException(f"Не удалось обработать количество {amount}!")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        price = json.loads(r.content)[keys[base]]
        return price

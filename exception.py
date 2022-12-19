import requests
import telebot

from config import a, val

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price (value: list, message: telebot.types.Message):
        if len(value) > 3:
            raise APIException('Введено слишком много параметров.\nОзнакомьтес, пожалуйста, с инструкцией повторно!\n/help')
        elif len(value) < 2:
            raise APIException('Введено не достаточно параметров.\n Ознакомьтес, пожалуйста, с инструкцией повторно!\n/help')

        try:
            base, quote, amount = value
        except ValueError:
            base, quote = value
            amount = '1'

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: "{amount}". Введите, пожалуйста число!')

        if quote == base:
            raise APIException(f'Нельзя конвертировать валюту саму в себя ({base} -> {base}) 🤷\n/help')

        try:
            quote_ticker = val[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: "{quote}".\nУбедитесь в парвильности написания!\n/help  /values')

        try:
            base_ticker = val[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: "{base}".\n Убедитесь в парвильности написания!\n/help  /values')

        r = requests.request(
            "GET",
            f'https://api.apilayer.com/fixer/convert?to={quote_ticker}&from={base_ticker}&amount={amount}',
            headers=a
        )

        return [amount, r]

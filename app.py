import telebot

import json
import time
import random

from config import TOKEN, val, wrong, asum, answ
from exception import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def hello(message: telebot.types.Message):
    text = 'Привет, я - бот-конвертер ConvBot!🤖\nИ я помогу тебе сравнить интересующую тебя валюту!💪\n\
Для этого пришли мне запрос в виде:\n  <имя валюты, ИЗ которой будем переводить>\
<имя валюты, В которую будем переводить> <количество переводимой валюты>\n\
Данные указывай через пробел☝\n\n\
Пример ввода: "доллар рубль 3"\n\n\
Всё остальное я сделаю сам!☺\n\n\
Список доступных для конвертации валют можно получить по команде /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for keys in val.keys():
        text = '\n'.join((text, keys, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    print(message.chat.username, message.text)
    try:
        value = message.text.lower().split(' ')
        converted = Converter.get_price(value, message)
    except APIException as e:
        bot.reply_to(message, f'{wrong[random.randint(1,5)]}\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Шестерёнки болят что-то ⚙💥... Обратись попозже...\n{e}')
    else:
        text = f'{converted[0]} {json.loads(converted[1].content)["query"]["from"]} \
        - {json.loads(converted[1].content)["result"]} {json.loads(converted[1].content)["query"]["to"]}'
        bot.send_message(message.chat.id, asum[random.randint(1,3)])
        time.sleep(random.randint(1,4))
        bot.send_message(message.chat.id, answ[random.randint(1,3)])
        bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)

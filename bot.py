
import telebot
from config import TOKEN,keys
from extensions import APIException, CriptoConvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Чтобы узнать цену валюты, введите сообщение в формате: '
                          '<имя валюты> <имя валюты, в которой надо узнать цену> <количество>.\n'
                          'Например: "доллар рубль 10".\n'
                          'Команда /values для просмотра доступных валют.')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    variables = message.text.split(' ')

    try:
        if len(variables) != 3:
            raise APIException('Неправильное количество параметров')

        quote,base,amount = variables
        total_base = CriptoConvertor.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message , f'Не удалось обработать команду \n {e}')
    else:
        total_base *= int(amount)
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
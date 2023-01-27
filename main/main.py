import telebot
from config import TOKEN, keys
from extensions import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    text = "Чтобы перевести валюту введите данные в следующем формате: " \
           "\n<название валюты> <в какую валюту переводить> <количество валюты>." \
           "\n Для того чтобы увидеть список валют введите:/values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values_handler(message):
    text = "Доступная валюта:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def conversion_handler(message):
    values = message.text.lower().split(" ")
    if len(values) == 2:
        #Этот блок нужен для того, что бы не писать количество валюты, если оно равно 1.
        try:
            quote, base = values
            price = CurrencyConverter.converter(quote, base)
        except ConversionException as e:
            bot.reply_to(message, f"Ошибка:\n{e}")
        except Exception as e:
            bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
        else:
            text = f"Цена 1 {quote} в {base} - {price}"
            bot.send_message(message.chat.id, text)
    else:
        try:
            if len(values) != 3:
                raise ConversionException("Неверное количество параметров!")
            quote, base, amount = values
            price = CurrencyConverter.converter(quote, base, amount)
        except ConversionException as e:
            bot.reply_to(message, f"Ошибка:\n{e}")
        except Exception as e:
            bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
        else:
            amount_val = float(price) * float(amount)
            text = f"Цена {amount} {quote} в {base} - {round(amount_val, 2)}"
            bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)

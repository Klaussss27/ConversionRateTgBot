import telebot
from currency_converter import CurrencyConverter
from telebot import types
import requests



bot = telebot.TeleBot('6510267027:AAHRlnnMliaTfeHmjuMAd2AYQMpuKeSp7HU')
amount = 0
currency = CurrencyConverter()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Input your amount")
    bot.register_next_step_handler(message, sum)

def sum(message):
    global amount
    try:
        amount = message.text.strip()
    except ValueError:
      bot.send_message(message.chat.id, "Please enter a valid amount.")
      bot.register_next_step_handler(message, sum)
      return


        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Other', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Choose the currency conversion", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Input your amount, it must be greater than zero.")
        bot.register_next_step_handler(message, sum)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    values = call.data.upper().split('/')
    res = currency.convert(amount,values[0],values[1])
    bot.send_message(call.message.chat.id, f'Result: {res}. You can type the sum again')
    bot.register_next_step_handler(call.message, sum)


bot.polling(none_stop=True)

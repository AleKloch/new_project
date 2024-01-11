import telebot
from config import TOKEN, exchanges
from extensions import Convertor, APIException
from telebot import types

def conv_markup(base = None):
    marcup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in exchanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.upper()))
    marcup.add(*buttons)
    return marcup

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = ("Привет. Я ONLINE-конвертор валют. "
            "Для того, чтобы узнать как я работаю, введите команду /help "
            "или продолжайте работу производя ввод команды /convert.")
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = ("Бот возвращает цену на определенное количество валюты (евро, доллар,юань или рубль)."
            " Ввод команды /values показывает перечень доступных для конвертации валют."
            "Нажмите на кнопку - валюта,цену которой хочется знать."
            " Далее нажмите на кнопку - имя валюты, в которой надо знать цену первой валюты."
            " Далее наберите количество первой валюты.")
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text = 'Доступные валюты для конвертации командой /convert:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values (message: telebot.types.Message):
    text = 'Выберите валюту для конвертации'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберите валюту в которую будем конвертировать'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Выберите количество конвектируемой валюты'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        round_price = Convertor.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации:\n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} равна: {round_price}"
        bot.send_message(message.chat.id, text)




bot.polling()
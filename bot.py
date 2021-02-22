import random
import telebot
import pyowm
from pyowm.utils.config import get_default_config
from telebot import types, TeleBot


config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = pyowm.OWM('793ed1da3cfd73fda377d706214f391d')
mgr = owm.weather_manager()
bot: TeleBot = telebot.TeleBot('1627697006:AAGp-IqYUWAUwFmVv-ps4E6q_YnxiExIXaM')


@bot.message_handler(commands=['start'])
def welcome(message, markup=None):
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # Кнопочки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число 🎲")
    item2 = types.KeyboardButton("🤔 Как дела? 🤔")
    item3 = types.KeyboardButton("Погода")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Дарова, {0.first_name} \nЯ - <b>{1.first_name}</b>, напиши название своего города".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.chat.type == 'private':
        if message.text == "🎲 Рандомное число 🎲":
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == "🤔 Как дела? 🤔":

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Всё хорошо, а у тебя?", reply_markup=markup)
        elif message.text == "Погода":
            send_message1(message)


def send_message1(message):
    bot.send_message(message.chat.id, "Введи название города, в котором хочешь узнать погоду")

    observation = mgr.weather_at_place(message.text)
    weather = observation.weather
    temp_dict = weather.temperature('celsius')
    temp = temp_dict['temp']

    answer = "В городе " + message.text + " сейчас " + weather.detailed_status + "\n"
    answer += "Температура: " + str(temp) + "°C\n\n"

    if temp < 0:
        answer += "❄ Холодно, одевайся как можно теплее ❄"
    elif temp < 20:
        answer += "⛅ Прохладно, приоденься ⛅"
    else:
        answer += "☀ Одевайся как хочешь, погода шик ☀"

    bot.send_message(message.chat.id, answer)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, "Хорошечно")
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, "умвачесей")

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="🤔 Как дела? 🤔",
                                      reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)

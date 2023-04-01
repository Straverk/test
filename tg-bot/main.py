import telebot
import sqlite3 as sl
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot('6193487447:AAGsq4ecSwe3A7Gesofb6kfXBxG7KVuZw6I')

msr_len = 0


def main_m(uid, s):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Создать заметку📋')
    btn2 = types.KeyboardButton('Редактировать заметку✏')
    markup.add(btn1, btn2)
    bot.send_message(uid, s, reply_markup=markup)


def create_n(uid, on, t):
    d = {1: "😭", 2: "😞", 3: "😐", 4: "😃", 5: "😁"}
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Отменить❌', callback_data="close"))

    if on < 2:
        markup.add(InlineKeyboardButton(text=f"{on}/5:{d[on]}✅", callback_data=f"confirm{on}"),
                   InlineKeyboardButton(text='➡', callback_data=f"lr{on + 1}"))
    elif on > 4:
        markup.add(InlineKeyboardButton(text='⬅', callback_data=f"lr{on - 1}"),
                   InlineKeyboardButton(text=f"{on}/5:{d[on]}✅", callback_data=f"confirm{on}"))
    else:
        markup.add(InlineKeyboardButton(text='⬅', callback_data=f"lr{on - 1}"),
                   InlineKeyboardButton(text=f"{on}/5:{d[on]}✅", callback_data=f"confirm{on}"),
                   InlineKeyboardButton(text='➡', callback_data=f"lr{on + 1}"))

    s = "На сколько вы оцениваете сегодняшний день📈\nНе забудьте написать заметку!"
    if t != -1:
        bot.edit_message_text(s, reply_markup=markup, chat_id=uid, message_id=t)
    else:
        bot.send_message(uid, s, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        s = "CREATE TABLE u" + str(message.from_user.id) + """(
                day INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT DEFAULT 'Нет заметки',
                mood INTEGER
                editnow integers DEFAULT 0
            );"""
        sl.connect('mood.db').cursor().execute(s)
    except BaseException:
        main_m(message.from_user.id, "Бот был перезапущен, и сейчас он готов к своей работе на все 100!")

    else:
        main_m(message.from_user.id, "Привет👋 Я ботик для ежедневных записей настроения, предлагаю начать создание"
                                     " твоей первой записи!")
    bot.send_message(message.from_user.id, str(message.message_id.date))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    if req[0] == 'close':
        main_m(call.message.chat.id, "Хорошо, удаляем запись👌")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif 'lr' in req[0]:
        s = req[0]
        create_n(call.message.chat.id, int(s[2]), call.message.message_id)

    if 'confirm' in req[0]:
        pass
        # sl.connect('mood.db').cursor().execute(f"""
        #    INSERT INTO u{str(call.message.chat.id)} VALUES
        #        ('Monty Python and the Holy Grail', 1975, 8.2)
        # """)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Создать заметку📋":
        create_n(message.from_user.id, 3, -1)


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть

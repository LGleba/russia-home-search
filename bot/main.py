import sqlite3
import telebot
from telebot import types
import random

# Python file with Telegram token
import config
# Python file with Parser
from AdsParser import Parser, Ad


# Reset user's request
def reset(telegram_id):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Request into databse. Update user's parameters
    cursor.execute(f"UPDATE users SET choice = ?, buy = ?, city = ?, metro = ?, house_type = ?, price_min = ?, price_max = ? WHERE telegram_id = ?",
        (0,
         'snyat',
         'Москва',
         '',
         'kvartira',
         '10000',
         '100000',
         telegram_id))
    # Save changes in database
    conn.commit()


# Create record in database if not exists
def putUserIfNotInBase(telegram_id):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Request into databse. Choose user
    cursor.execute(f"SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
    # If user is not in database
    if not cursor.fetchone():
    	# Add user's record
        cursor.execute(f"INSERT INTO users (telegram_id, choice, buy, city, metro, house_type, price_min, price_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (telegram_id,
                        0,
                        'snyat',
                        'Москва',
                        '',
                        'kvartira',
                        '10000',
                        '100000',))
        # Save changes in database
        conn.commit()


# Get user's parameters
def getParams(telegram_id):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Get parameters
    cursor.execute(f"SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    # return parameters
    return cursor.fetchone()


# Update user's choice in record
def putChoice(telegram_id, choice):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Update parameter in user's record
    cursor.execute(f"UPDATE users SET choice = ? WHERE telegram_id = ?", (choice, telegram_id))
    # Save changes in database
    conn.commit()


# Update user's city in record
def putCity(telegram_id, city):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Update parameter in user's record
    cursor.execute(f"UPDATE users SET city = ? WHERE telegram_id = ?", (city, telegram_id))
    # Save changes in database
    conn.commit()


# Update user's metro in record
def putMetro(telegram_id, metro):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Update parameter in user's record
    cursor.execute(f"UPDATE users SET metro = ? WHERE telegram_id = ?", (metro, telegram_id))
    # Save changes in database
    conn.commit()


# Update user's "price min" in record
def putPriceMin(telegram_id, price_min):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Update parameter in user's record
    cursor.execute(f"UPDATE users SET price_min = ? WHERE telegram_id = ?", (price_min, telegram_id))
    # Save changes in database
    conn.commit()


# Update user's "price max" in record
def putPriceMax(telegram_id, price_max):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Update parameter in user's record
    cursor.execute(f"UPDATE users SET price_max = ? WHERE telegram_id = ?", (price_max, telegram_id))
    # Save changes in database
    conn.commit()


# Update user's "buy" in record
def putBuy(telegram_id, buy):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Update parameter in user's record
    cursor.execute(f"UPDATE users SET buy = ? WHERE telegram_id = ?", (buy, telegram_id))
    # Save changes in database
    conn.commit()


# Update user's "house type" in record
def putHouseType(telegram_id, house_type):
	# Connect to database
    conn = sqlite3.connect('users.sqlite')
    # Create cursor in database
    cursor = conn.cursor()
    # Update parameter in user's record
    cursor.execute(f"UPDATE users SET house_type = ? WHERE telegram_id = ?", (house_type, telegram_id))
    # Save changes in database
    conn.commit()


# Token Telegram
API_TOKEN = config.API_TOKEN
# Init Telegram-bot
bot = telebot.AsyncTeleBot(API_TOKEN)
# Text which was sending after user's answer
TEXT = ["Интерсно что ты хочешь найти...",
        "Допустим записал",
        "Записал мой господин",
        "Ты меня интригуешь",
        "Крутой выбор",
        "Люк, я твой отец. Блин, извини, смотрю Звездные войны",
        "Уже устал смотреть сериалы на карантине",
        "Понял, принял, записал",
        "Блин, у меня один Позитив не прошел в Jobs",
        "Снова Вы, отвлекаете меня от важного дела, сериалы сами себя не посмотрят",
        "Было бы здорово помочь тебе",
        "Да записываю я, спокойно",
        "2 + 2 = 5",
        "Я тоже решил найти убежище от Коровавируса",
        "Надеюсь, я тебе нравлюсь",
        "Хорошо, что я не могу заболеть Коровавирусом, ведь боты не болеют",
        "Хмм...",
        "OK",
        "Надеюсь, ты не просто так кнопочки нажимаешь!",
        "Дайте поспать, боты тоже люди. Упс ошибочка вышла. Ты ничего не видел"]


# Command /start, /help
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Buttons
    item0 = types.KeyboardButton("Какой мой запрос?")
    item1 = types.KeyboardButton("Изм. (снять/купить)")
    item2 = types.KeyboardButton("Изм. город")
    item3 = types.KeyboardButton("Изм. (дом/квартира)")
    item4 = types.KeyboardButton("Изм. метро")
    item5 = types.KeyboardButton("Изм. цену от")
    item6 = types.KeyboardButton("Изм. цену до")
    item7 = types.KeyboardButton("Вывести таблицу")
    # Add buttons in Telegram
    markup.add(item0, item1, item2, item3, item4, item5, item6, item7)
    # Welcome message
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, я бот, который умеет находить объявления недвижимости и выводить их пользователю", reply_markup=markup)


# User's text
@bot.message_handler(content_types=['text'])
def echo_message(message):
	# Add user's record if not exists
    putUserIfNotInBase(message.from_user.id)
    # Check private
    if message.chat.type == 'private':
        # User's choice = 1
        if getParams(message.from_user.id)[2] == 1:
        	# Reset choice
            putChoice(message.from_user.id, 0)
            # Update user's city
            putCity(message.from_user.id, message.text)
            # Send message with random text
            bot.send_message(message.chat.id, random.choice(TEXT))
        # User's choice = 2
        elif getParams(message.from_user.id)[2] == 2:
        	# Reset choice
            putChoice(message.from_user.id, 0)
            # Update user's metro
            putMetro(message.from_user.id, message.text)
            # Send message with random text
            bot.send_message(message.chat.id, random.choice(TEXT))
        # User's choice = 3
        elif getParams(message.from_user.id)[2] == 3:
        	# Reset choice
            putChoice(message.from_user.id, 0)
            try:
            	# Update user's "price min"
                putPriceMin(message.from_user.id, str(int(message.text)))
                # Send message with random text
                bot.send_message(message.chat.id, random.choice(TEXT))
            except:
            	# Send message with Error
                bot.send_message(message.chat.id, "Извините, но кажется, Вы ошиблись при вводе")
        # User's choice = 4
        elif getParams(message.from_user.id)[2] == 4:
        	# Reset choice
            putChoice(message.from_user.id, 0)
            try:
            	# Update user's "price max"
                putPriceMax(message.from_user.id, str(int(message.text)))
                # Send message with random text
                bot.send_message(message.chat.id, random.choice(TEXT))
            except:
            	# Send message with Error
                bot.send_message(message.chat.id, "Извините, но кажется, Вы ошиблись при вводе")

        # User wants to know his request
        if message.text == "Какой мой запрос?":
        	# Keyboard
            markup = types.InlineKeyboardMarkup(row_width=1)
            # Button
            item1 = types.InlineKeyboardButton('Сбросить параметры', callback_data='reset')
            # Add button
            markup.add(item1)
            # Send to user about his request
            bot.send_message(message.chat.id, f"Ваш запрос:\n"
                                              f"Тип (снять/купить): {getParams(message.from_user.id)[3]},\n"
                                              f"Город: {getParams(message.from_user.id)[4]},\n"
                                              f"Тип (дом/квартира): {getParams(message.from_user.id)[6]},\n"
                                              f"Метро: {getParams(message.from_user.id)[5]},\n"
                                              f"Цена от: {getParams(message.from_user.id)[7]},\n"
                                              f"Цена до: {getParams(message.from_user.id)[8]}.", reply_markup=markup)
            # Reset choice
            putChoice(message.from_user.id, 0)
        # User wants to change buy
        elif message.text == "Изм. (снять/купить)":
        	# Keyboard
            markup = types.InlineKeyboardMarkup(row_width=2)
            # Buttons
            item1 = types.InlineKeyboardButton('Снять', callback_data='snyat')
            item2 = types.InlineKeyboardButton('Купить', callback_data='kupit')
            # Add buttons
            markup.add(item1, item2)
            # Send message about buy
            bot.send_message(message.chat.id, "Выберите тип (снять/купить):", reply_markup=markup)
            # Reset choice
            putChoice(message.from_user.id, 0)
        # User wants to change city
        elif message.text == "Изм. город":
        	# Send message about city
            bot.send_message(message.chat.id, "Напишите город:")
            # Put choice 1
            putChoice(message.from_user.id, 1)
        # User wants to change house type
        elif message.text == "Изм. (дом/квартира)":
        	# Keyboard
            markup = types.InlineKeyboardMarkup(row_width=2)
            # Buttons
            item1 = types.InlineKeyboardButton('Квартира', callback_data='kvartira')
            item2 = types.InlineKeyboardButton('Дом', callback_data='dom')
            # Add buttons
            markup.add(item1, item2)
            # Send message about house type
            bot.send_message(message.chat.id, "Выберите тип (дом/квартира):", reply_markup=markup)
            # Reset choice
            putChoice(message.from_user.id, 0)
        # User wants to change metro
        elif message.text == "Изм. метро":
        	# Send message about metro
            bot.send_message(message.chat.id, "Напишите метро:")
            # Put choice 2
            putChoice(message.from_user.id, 2)
        # User wants to change "price min"
        elif message.text == "Изм. цену от":
        	# Send message about "price min"
            bot.send_message(message.chat.id, "Напишите цену от:")
            # Put choice 3
            putChoice(message.from_user.id, 3)
        # User wants to change "price max"
        elif message.text == "Изм. цену до":
        	# Send message about "price max"
            bot.send_message(message.chat.id, "Напишите цену до:")
            # Put choice 4
            putChoice(message.from_user.id, 4)
        # User wants to see his request
        elif message.text == "Вывести таблицу":
        	# Send message about start to find home
            bot.send_message(message.chat.id, "Начинаю поиск...")
            # Create Parser and set user's parameters from database
            parser = Parser(city=getParams(message.from_user.id)[4],
                            buy=getParams(message.from_user.id)[3],
                            house_type=getParams(message.from_user.id)[6],
                            price_min=getParams(message.from_user.id)[7],
                            price_max=getParams(message.from_user.id)[8],
                            metro=getParams(message.from_user.id)[5])
            # Set max count of adds
            parser.page_init_yandex(15)
            # Work with every add
            for k in range(15):
                try:
                	# Get add
                    i = parser.get_ad_yandex(k)
                    # Send add to user
                    bot.send_message(message.chat.id, "~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                                      f"| {i.title}\n"
                                                      f"| {i.address}\n"
                                                      f"| {i.price}\n"
                                                      f"| {i.url}")
                    # Succesful operation
                    putChoice(message.from_user.id, 5)
                except:
                	# Stop cycle
                    break
            # If not succesful find
            if (getParams(message.from_user.id)[2] != 5):
            	# Send to user with Error
                bot.send_message(message.chat.id, "Ничего не нашел ;(\n"
                                                  "Проверьте свой запрос")
            # Reset choice
            putChoice(message.from_user.id, 0)


# Work with calls
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
    	# Reset message
        if call.data == 'reset':
        	# Reset user's record
            reset(call.message.chat.id)
            # Send to user about reset record
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Сбросил данные",
                                  reply_markup=None)
            # Send to user about new his request
            bot.send_message(message.chat.id, f"Ваш запрос:\n"
                                              f"Тип (снять/купить): {getParams(message.from_user.id)[3]},\n"
                                              f"Город: {getParams(message.from_user.id)[4]},\n"
                                              f"Тип (дом/квартира): {getParams(message.from_user.id)[6]},\n"
                                              f"Метро: {getParams(message.from_user.id)[5]},\n"
                                              f"Цена от: {getParams(message.from_user.id)[7]},\n"
                                              f"Цена до: {getParams(message.from_user.id)[8]}.")
        # Set buy
        elif call.data == 'snyat':
        	# Set user's buy
            putBuy(call.message.chat.id, 'snyat')
            # Send to user about update buy
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Изменен тип на 'Снять'",
                                  reply_markup=None)
        # Set buy
        elif call.data == 'kupit':
        	# Set user's buy
            putBuy(call.message.chat.id, 'kupit')
            # Send to user about update buy
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Изменен тип на 'Купить'",
                                  reply_markup=None)
       	# Set house type
        elif call.data == 'kvartira':
        	# Set user's house type
            putHouseType(call.message.chat.id, 'kvartira')
            # Send to user about update house type
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Изменен тип на 'Квартира'",
                                  reply_markup=None)
        # Set house type
        elif call.data == 'dom':
        	# Set user's house type
            putHouseType(call.message.chat.id, 'kvartira')
            # Send to user about update house type
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Изменен тип на 'Дом'",
                                  reply_markup=None)


# Bot polling
bot.polling()

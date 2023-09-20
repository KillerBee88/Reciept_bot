import os
from dotenv import load_dotenv
import telebot

load_dotenv()

BOT_TOKEN = os.getenv('TG_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    bot.send_message(chat_id=message.chat.id, text=f"Привет, {user.first_name}! Чем я могу помочь?")
    
    # Создаем инлайн-кнопку для получения списка рецептов
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("Получить список рецептов", callback_data='recipe_list'))
    bot.send_message(chat_id=message.chat.id, text="Нажмите на кнопку, чтобы получить список рецептов:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def button(call):
    selected_option = call.data

    if selected_option == 'recipe_list':
        # Создаем инлайн-кнопки для выбора типа рецептов
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(telebot.types.InlineKeyboardButton("Без глютена", callback_data='gluten_free'))
        keyboard.row(telebot.types.InlineKeyboardButton("Веганское", callback_data='vegan'))
        keyboard.row(telebot.types.InlineKeyboardButton("Эко", callback_data='eco'))

        # Отправляем пользователю сообщение с кнопками
        bot.send_message(chat_id=call.message.chat.id, text="Выберите тип рецептов:", reply_markup=keyboard)
    elif selected_option == 'gluten_free':
        bot.send_message(chat_id=call.message.chat.id, text="Список рецептов без глютена: ...")
    elif selected_option == 'vegan':
        bot.send_message(chat_id=call.message.chat.id, text="Список веганских рецептов: ...")
    elif selected_option == 'eco':
        bot.send_message(chat_id=call.message.chat.id, text="Список экологичных рецептов: ...")


bot.polling()
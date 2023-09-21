import random
from django.core.management.base import BaseCommand
from reciept_bot.settings import TELEGRAM_TOKEN
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from recipe.models import Recipe, Subscription, Categories, Client, LikeDislike, UserCategoryView

bot = TeleBot(TELEGRAM_TOKEN, threaded=False)


@bot.message_handler(commands=['start'])
def main_menu(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    welcome_message = f'Привет, {message.from_user.username}!\nДля того, чтобы продолжить пользоваться ботом ' \
                      f'просим вас оплатить подписку стоимостью 100 эфиопских тугриков'
    kb_welcome = ReplyKeyboardMarkup(one_time_keyboard=True)
    kb_welcome_btn = (
        KeyboardButton(text='Оплатить 🚫'),
        KeyboardButton(text='Уже оплатил 🚻'),
    )
    kb_welcome.add(*kb_welcome_btn)
    bot.send_message(message.chat.id, welcome_message, reply_markup=kb_welcome)


@bot.message_handler(func=lambda message: message.text == 'Оплатить 🚫')
def handle_payment(message):
    bot.send_message(message.chat.id, 'Закрыто на техобслуживание')


@bot.message_handler(func=lambda message: message.text == 'Уже оплатил 🚻')
def handle_backdoor(message):

    client = Client.objects.get_or_create(tg_id=message.from_user.id)[0]
    client.name = message.from_user.first_name
    client.username = message.from_user.username
    client.save()

    kb_main_menu = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_main_menu_btn = (
        KeyboardButton(text='Получить персональный рецепт блюда 🍔🍟🥩'),
        KeyboardButton(text='Мой профиль 🆔'),
        KeyboardButton(text='Мои топовые рецепты 🧡')
    )

    kb_main_menu.add(*kb_main_menu_btn)
    bot.send_message(message.chat.id, 'Спасибо за оплату подписки на 30 дней!', reply_markup=kb_main_menu)


@bot.message_handler(func=lambda message: message.text == 'Получить персональный рецепт блюда 🍔🍟🥩')
def handle_category(message):
    kb_category = ReplyKeyboardMarkup()
    kb_category_btn = (
        KeyboardButton(text='Супы'),
        KeyboardButton(text='Горячее блюдо'),
        KeyboardButton(text='Десерт')
    )
    kb_category.add(*kb_category_btn)
    bot.send_message(message.chat.id, 'Пожалуйста, выберите желаемую категорию блюда', reply_markup=kb_category)


@bot.message_handler(func=lambda message: message.text == 'Супы')
def handle_soup_category(message):
    soup_recipe = get_random_recipe('Супы')
    bot.send_message(message.chat.id, f'Вот рецепт супа:\n{soup_recipe}')


@bot.message_handler(func=lambda message: message.text == 'Горячее блюдо')
def handle_hot_dish_category(message):
    hot_dish_recipe = get_random_recipe('Горячее блюдо').title
    bot.send_message(message.chat.id, f'Вот рецепт горячего блюда:\n{hot_dish_recipe}')


@bot.message_handler(func=lambda message: message.text == 'Десерт')
def handle_dessert_category(message):
    dessert_recipe = get_random_recipe('Десерт').title
    bot.send_message(message.chat.id, f'Вот рецепт десерта:\n{dessert_recipe}')


def get_random_recipe(category_name):
    category = Categories.objects.get(category=category_name)
    recipes = Recipe.objects.filter(category=category)
    recipe = random.choice(recipes)
    return recipe


def main():
    bot.polling(skip_pending=True)


class Command(BaseCommand):
    help = 'Телеграм бот для предоставления рецептов по подписке'

    def handle(self, *args, **options):
        while True:
            try:
                main()
            except Exception as error:
                print(error)
                raise SystemExit


if __name__ == '__main__':
    main()

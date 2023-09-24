import datetime
import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from reciept_bot.settings import TELEGRAM_TOKEN
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from recipe.models import Recipe, Subscription, Categories, Client, LikeDislike, UserLimitView
from io import BytesIO
import json


bot = TeleBot(TELEGRAM_TOKEN, threaded=False)


@bot.message_handler(commands=['start'])
def main_menu(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    welcome_message = f'Привет, {message.from_user.username}!\nПолучи интересный рецепт и разнообразь свое меню'
    client = Client.objects.get_or_create(tg_id=message.from_user.id)[0]
    client.name = message.from_user.first_name
    client.username = message.from_user.username
    client.save()
    subscription = Subscription.objects.filter(client=client)
    if not subscription.exists():
        Subscription.objects.create(client=client, subscription_is_active=False)
        UserLimitView.objects.create(user=client)

    kb_main_menu = get_main_menu_kb()
    bot.send_message(message.chat.id, welcome_message, reply_markup=kb_main_menu)


@bot.message_handler(func=lambda message: message.text == 'Мой профиль 🆔')
def get_profile_info(message):
    client = Client.objects.get(tg_id=message.from_user.id)

    subscription_duration = Subscription.objects.get(client=client).subscription_duration
    update_subscription_time(subscription_duration, client)
    duration = format_duration(subscription_duration)
    subscription_is_active = Subscription.objects.get(client=client).subscription_is_active
    vegan = client.vegetarian
    if subscription_is_active:
        profile_msg = f'Ваш профиль\n' \
                      f'Подписка истекает через:\n ' \
                      f'{duration}'
        kb_profile = ReplyKeyboardMarkup(resize_keyboard=True)
        if vegan:
            vegan_btn = KeyboardButton(text='Выключить режим "Травоядный"')
        else:
            vegan_btn = KeyboardButton(text='Включить режим "Травоядный"')

        kb_profile_btn = [
            KeyboardButton(text='Продлить подписку'),
            vegan_btn,
            KeyboardButton(text='Назад в основное меню 🔙')
        ]
        kb_profile.add(*kb_profile_btn)
    else:
        view_limit = UserLimitView.objects.get(user=client)
        profile_msg = f'У вас отсутствует активная подписка.\n' \
                      f'У вас осталось {view_limit.views_left} просмотр(а)\n' \
                      f'Нажмите на кнопу "Приобрести подписку" для ее приобретения'

        kb_profile = ReplyKeyboardMarkup(resize_keyboard=True)
        kb_profile_btn = [
            KeyboardButton(text='Приобрести подписку'),
            KeyboardButton(text='Включить режим "Травоядный"'),
            KeyboardButton(text='Назад в основное меню 🔙')
        ]
        kb_profile.add(*kb_profile_btn)

    bot.send_message(message.chat.id, profile_msg, reply_markup=kb_profile)


@bot.message_handler(func=lambda message: message.text == 'Включить режим "Травоядный"')
def handler_activate_killer_mode(message):
    client = Client.objects.get(tg_id=message.from_user.id)
    client.vegetarian = True
    client.save()
    kb_main = get_main_menu_kb()
    bot.send_message(message.chat.id, 'Режим "асасин" активирован', reply_markup=kb_main)


@bot.message_handler(func=lambda message: message.text == 'Выключить режим "Травоядный"')
def handler_deactivate_killer_mode(message):
    client = Client.objects.get(tg_id=message.from_user.id)
    client.vegetarian = False
    client.save()
    kb_main = get_main_menu_kb()
    bot.send_message(message.chat.id, 'Режим "асасин" деактивирован', reply_markup=kb_main)


@bot.message_handler(func=lambda message: message.text == 'Мои топовые рецепты 🧡')
def handler_get_my_top_recipes(message):
    kb_main = get_main_menu_kb()
    client = Client.objects.get(tg_id=message.from_user.id)
    top_recipes = LikeDislike.objects.filter(client=client)
    if top_recipes.exists():
        recipes = [like.recipe for like in top_recipes]
        page = 1
        count = len(recipes)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                   InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'{{"method": "pagination",'
                                                                           f'"NumberPage": {page+1}, '
                                                                           f'"CountPage": {count}}}'
    ))
        bot.send_message(message.from_user.id, f'<b>{recipes[page-1].title}</b>\n\n'
                                               f'Время приготовления:\n{recipes[page-1].cooking_time} минут\n\n'
                                               f'Способ приготовления:\n{recipes[page-1].description}\n\n'
                                               f'Ингридиенты:\n{recipes[page-1].ingredients}\n\n'
                                               f'Стоимость ингридиентов:\n{recipes[page-1].price} тугриков',

                         reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(message.from_user.id, 'Извините, у вас отсутствуют топ рецепты', reply_markup=kb_main)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    client = Client.objects.get(tg_id=call.from_user.id)
    top_recipes = LikeDislike.objects.filter(client=client)
    recipes = [like.recipe for like in top_recipes]
    req = call.data.split('_')
    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        if page == 1:
            markup.add(
                InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                InlineKeyboardButton(text=f'Вперёд --->',
                                     callback_data=f'{{"method":"pagination","NumberPage":{page + 1},'
                                                   f'"CountPage":{count}}}')
            )
        elif page == count:
            markup.add(InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data=f'{{"method":"pagination","NumberPage":{page - 1},'
                                                          f'"CountPage": {count}}}'
),

                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
        else:
            markup.add(InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data=f'{{"method":"pagination","NumberPage":{page - 1},'
                                                          f'"CountPage": {count}}}'),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data=f'{{"method":"pagination","NumberPage":{page + 1},'
                                                          f'"CountPage":{count}}}'))
        bot.edit_message_text(f'<b>{recipes[page-1].title}</b>\n\n'
                              f'Время приготовления:\n{recipes[page-1].cooking_time} минут\n\n'
                              f'Способ приготовления:\n{recipes[page-1].description}\n\n'
                              f'Ингридиенты:\n{recipes[page-1].ingredients}\n\n'
                              f'Стоимость ингридиентов:\n{recipes[page-1].price} тугриков',

                              reply_markup=markup,
                              parse_mode='HTML',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


@bot.message_handler(func=lambda message: message.text == 'Приобрести подписку' or message.text == 'Продлить подписку')
def buy_subscription(message):
    kb_subscription = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_subscription_btn = (
        KeyboardButton(text='1️⃣ день'),
        KeyboardButton(text='7️⃣ дней'),
        KeyboardButton(text='3️⃣0️⃣ дней'),
        KeyboardButton(text='Назад в основное меню 🔙')
    )
    kb_subscription.add(*kb_subscription_btn)
    bot.send_message(message.chat.id, 'Выберите жилаемый период подписки', reply_markup=kb_subscription)


@bot.message_handler(func=lambda message: message.text == '1️⃣ день' or message.text == '7️⃣ дней' or
                     message.text == '3️⃣0️⃣ дней')
def pay_subscription(message):
    client = Client.objects.get(tg_id=message.from_user.id)
    subscription = Subscription.objects.get(client=client)
    subscription.subscription_duration = timedelta(days=0)
    if message.text == '1️⃣ день':
        subscription.subscription_duration += timedelta(days=1)
        subscription.subscription_price += Decimal(10.00)
    elif message.text == '7️⃣ дней':
        subscription.subscription_duration += timedelta(days=7)
        subscription.subscription_price += Decimal(16.49)
    elif message.text == '3️⃣0️⃣ дней':
        subscription.subscription_duration += timedelta(days=30)
        subscription.subscription_price += Decimal(25.99)

    kb_main_menu = get_main_menu_kb()
    subscription.subscription_date = datetime.now()
    subscription.subscription_is_active = True
    subscription.save()
    pay_subscription_msg = f'Благодарим вас за покупку подписки на {message.text}'

    bot.send_message(message.chat.id, pay_subscription_msg, reply_markup=kb_main_menu)


@bot.message_handler(func=lambda message: message.text == 'Получить персональный рецепт блюда 🍔🍟🥩')
def handle_category(message):
    kb_category = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_category_btn = (
        KeyboardButton(text='Супы'),
        KeyboardButton(text='Горячее блюдо'),
        KeyboardButton(text='Десерт'),
        (KeyboardButton(text='Назад в основное меню 🔙'))

    )
    kb_category.add(*kb_category_btn)
    bot.send_message(message.chat.id, 'Пожалуйста, выберите желаемую категорию блюда', reply_markup=kb_category)


@bot.message_handler(func=lambda message: message.text == 'Назад в основное меню 🔙')
def back_to_main_menu(message):
    main_menu_message = 'Вы вернулись в основное меню'
    kb_main_menu = get_main_menu_kb()
    bot.send_message(message.chat.id, main_menu_message, reply_markup=kb_main_menu)


@bot.message_handler(func=lambda message: message.text.startswith('Скачать рецепт'))
def handler_load_recipe(message):
    recipe_title = message.text.split('Скачать рецепт "')[1].split('"')[0]
    ingredients = Recipe.objects.get(title=recipe_title).ingredients
    ingredients_txt_file = BytesIO(ingredients.encode('utf-8'))
    ingredients_txt_file.name = 'ingredients.txt'
    kb = get_main_menu_kb()
    bot.send_document(message.chat.id, ingredients_txt_file, caption=f'Ваши ингридиенты для '
                                                                     f'{recipe_title} в формате txt', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text.startswith('Получить ингредиенты для'))
def handle_get_ingredients(message):
    recipe_title = message.text.split('Получить ингредиенты для "')[1].split('"')[0]
    ingredients = Recipe.objects.get(title=recipe_title).ingredients
    kb_ingredients = ReplyKeyboardMarkup()
    kb_ingredients_btn = (
        KeyboardButton(text=f'Скачать рецепт "{recipe_title}"'),
        KeyboardButton(text='Назад в основное меню 🔙')
    )
    kb_ingredients.add(*kb_ingredients_btn)
    bot.send_message(message.chat.id, ingredients, reply_markup=kb_ingredients)


@bot.message_handler(func=lambda message: message.text.startswith('Добавить в мои топ рецепты'))
def handler_add_to_my_top_recipe(message):
    client = Client.objects.get(tg_id=message.from_user.id)
    recipe_title = message.text.split('Добавить в мои топ рецепты "')[1].split('"')[0]
    recipe = Recipe.objects.get(title=recipe_title)
    like = LikeDislike.objects.get_or_create(client=client, recipe=recipe, action=True)[0]
    like.save()
    bot.send_message(message.chat.id, f'Рецепт {recipe_title} успешно добавлен в ваши топ блюда')


@bot.message_handler(func=lambda message: message.text.startswith('Получить другой рецепт из категории'))
def handler_get_another_recipe(message):
    category = message.text.split('Получить другой рецепт из категории "')[1].split('"')[0]
    get_recipe(bot, message.chat.id, category)


@bot.message_handler(func=lambda message: message.text == 'Супы' or message.text == 'Горячее блюдо' or
                     message.text == 'Десерт')
def handle_recipe_category(message):
    client = Client.objects.get(tg_id=message.from_user.id)
    subscription_duration = Subscription.objects.get(client=client).subscription_duration
    update_subscription_time(subscription_duration, client)
    get_recipe(bot, message.chat.id, message.text)


def format_duration(duration):
    days, seconds = duration.days, duration.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    formatted_duration = f"{days:02d} дней:{hours:02d} часов:{minutes:02d} минут"
    return formatted_duration


def get_random_recipe(category_name, vegan):
    category = Categories.objects.get(category=category_name)
    recipes = Recipe.objects.filter(category=category, vegan_recipe=vegan)
    recipe = random.choice(recipes)
    cooking_time = f'Время приготовления: {recipe.cooking_time} минут'
    descr = f'Способ приготовления:\n{recipe.description}'
    return recipe, cooking_time, descr


def get_recipe(bot, chat_id, category):
    client = Client.objects.get(tg_id=chat_id)
    vegan = client.vegetarian
    subscription_active = Subscription.objects.get(client=client).subscription_is_active
    limit_view = UserLimitView.objects.get(user=client)

    if subscription_active or not subscription_active and limit_view.views_left > 0:
        recipe, cooking_time, descr = get_random_recipe(category, vegan)
        kb_additional_info = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        kb_add_info_btn = (
            KeyboardButton(text=f'Получить ингредиенты для "{recipe.title}"'),
            KeyboardButton(text=f'Добавить в мои топ рецепты "{recipe.title}"'),
            KeyboardButton(text=f'Получить другой рецепт из категории "{recipe.category}"'),
            KeyboardButton(text=f'Назад в основное меню 🔙'),

        )
        kb_additional_info.add(*kb_add_info_btn)

        bot.send_message(chat_id, f'Вот ваш рецепт:\n{recipe.title}')
        bot.send_photo(chat_id, recipe.image)
        bot.send_message(chat_id, cooking_time)
        bot.send_message(chat_id, descr, reply_markup=kb_additional_info)

        if not subscription_active:
            limit_view.views_left -= 1
            limit_view.save()
    else:
        kb_buy_subscription = ReplyKeyboardMarkup()
        kb_buy_subscription_btn = [
            KeyboardButton(text='Приобрести подписку'),
            KeyboardButton(text='Назад в основное меню 🔙')
        ]
        kb_buy_subscription.add(*kb_buy_subscription_btn)

        bot.send_message(chat_id, 'Извините, но бесплатные показы для вас закончились,\nчтобы продолжить '
                                  'приобретите подписку', reply_markup=kb_buy_subscription)


def get_main_menu_kb():
    kb_main_menu = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    kb_main_menu_btn = (
        KeyboardButton(text='Получить персональный рецепт блюда 🍔🍟🥩'),
        KeyboardButton(text='Мой профиль 🆔'),
        KeyboardButton(text='Мои топовые рецепты 🧡')
    )
    kb_main_menu.add(*kb_main_menu_btn)
    return kb_main_menu


def update_subscription_time(time: datetime, client: Client):
    now = timezone.now()
    subscription = Subscription.objects.get(client=client)
    subscription_time = subscription.subscription_date + time - now
    subscription.subscription_duration = subscription_time
    if subscription_time.total_seconds() <= 0:
        subscription.subscription_is_active = False
    subscription.save()


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

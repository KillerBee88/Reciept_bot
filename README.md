# Recipes Telegram Bot

Телеграм-бот для получения рецепта по категориям, с возможностью получить список ингредиентов к конкретному рецепту в формате `.txt`. Также реализована возможность добавлять рецепт в ваши топ рецепты. Обычный пользователь без подписки, имеет возможность получить без подписки только 3 рецептов. С подпиской нет лимитов на получение рецептов.

## Установка

```commandline
git clone https://github.com/KillerBee88/Reciept_bot.git
```

## Установка зависимостей
Переход в директорию с исполняемым файлом и установка

```commandline
cd Reciept_bot
```

Установка
```commandline
pip install -r requirements.txt
```

## Создание и настройка .env

Создайте в корне папки `Reciept_bot` файл `.env`. Откройте его для редактирования любым текстовым редактором и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны следующие переменные:
 - SECRET_KEY - секретный ключ проекта. Например: `erofheronoirenfoernfx49389f43xf3984xf9384`.
- ALLOWED_HOSTS - см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- DATABASE_URL- Например: postgresql://USER:PASSWORD@HOST:PORT/NAME. [Подробнее](https://github.com/jazzband/dj-database-url#url-schema)
- STATIC_URL - по умолчанию это `'/static/'`.  [Что такое STATIC_URL](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-STATIC_URL).
- STATIC_ROOT - по умолчанию это `'None'`, т.е. текущая папка. [Что такое STATIC_ROOT](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-STATIC_ROOT). 
- MEDIA_URL - по умолчанию это `'/media/'`. [Что такое MEDIA_URL](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-MEDIA_URL).
- MEDIA_ROOT - по умолчанию это `'media'`. [Что такое MEDIA_ROOT](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-MEDIA_ROOT).
- TELEGRAM_TOKEN - ваш телеграм бот API ключ


## Подготовка к запуску

1. Переходим в директорию с `manage.py`

```commandline
cd reciept_bot
```

2. Создаем миграции

```commandline
python manage.py makemigrations
```

3. Применяем миграции

```commandline
python manage.py migrate
```

4. Создаём суперпользователя

```commandline
python manage.py createsuperuser
```

## Запуск

Проект состоит из 2 частей:

- админки
- телеграм-бота

### Запуск админки

```commandline
python manage.py runserver
```

Перейдите по адресу http://127.0.0.1:8000/admin/ и введите данные для авторизации, которые вы указали ранее.  

### Запуск телеграм-бота

```commandline
python manage.py bot
```

Перейдите в вашего телеграм-бота, ключ, которого вы ранее указывали в файле `.env` и введите команду `/start`.

## Цели проекта
Код написан в рамках выполнения командного проекта в формате фриланс-заказа. 


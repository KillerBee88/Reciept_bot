from datetime import timedelta

from django.db import models


class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    title = models.CharField('Название рецепта', max_length=50, null=False)
    image = models.ImageField('Изображение', upload_to='images/', null=True)
    cooking_time = models.IntegerField('Время приготовления в минутах', null=True)
    description = models.TextField('Способ приготовления', max_length=3000)
    ingredients = models.TextField('Ингридиенты', max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vegan_recipe = models.BooleanField(verbose_name='Веганский рецепт')
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Client(models.Model):
    tg_id = models.BigIntegerField(verbose_name="ID пользователя")
    username = models.CharField(max_length=200, verbose_name="Username пользователя")
    name = models.CharField('Имя в тг', max_length=20, default='Клиент')
    vegetarian = models.BooleanField('Травоядное', default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_date = models.DateTimeField(verbose_name='Дата подписки', auto_now=True)
    subscription_is_active = models.BooleanField(verbose_name='Подписка', default=False)
    subscription_duration = models.DurationField(verbose_name='Длительность подписки', default=timedelta(days=0))
    subscription_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(verbose_name='Категория рецепта', max_length=20)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class LikeDislike(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    action = models.BooleanField(verbose_name='Действие пользователя', default=None)

    class Meta:
        unique_together = ['client', 'recipe', 'action']


class UserLimitView(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='category_views')
    views_left = models.IntegerField(default=3)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['user', 'date']

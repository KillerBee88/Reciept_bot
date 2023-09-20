from django.db import models


class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    title = models.CharField('Название рецепта', max_length=255, null=False)
    image = models.ImageField('Изображение', upload_to='images/', null=True)
    cooking_time = models.CharField('Время приготовления', max_length=100, null=True)
    description = models.CharField('Описание приготовления', max_length=500)
    ingredients = models.JSONField('Ингридиенты', null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vegan_recipe = models.BooleanField(verbose_name='Веганский рецепт')
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.ingredients}{self.price}'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField('Имя пользователя', max_length=20,  null=False)
    subscription = models.ForeignKey(
        'Subscription', on_delete=models.CASCADE, related_name='user_subscriptions')
    email = models.EmailField(
        'Адрес электронной почты', max_length=255, unique=True)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_is_active = models.BooleanField(verbose_name='Подписка')
    subscription_duration = models.DateTimeField(
        verbose_name='Длительность подписки', auto_now=False)
    subscription_price = models.DecimalField(max_digits=10, decimal_places=2)


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField('Категория рецепта', max_length=20)


class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    action = models.BooleanField(verbose_name='Действие пользователя')

    class Meta:
        unique_together = ['user', 'recipe', 'action']

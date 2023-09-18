# Generated by Django 4.2.5 on 2023-09-18 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                ("recipe_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(max_length=25, verbose_name="Название рецепта"),
                ),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to="images/", verbose_name="Изображение"
                    ),
                ),
                (
                    "cooking_time",
                    models.TimeField(null=True, verbose_name="Время приготовления"),
                ),
                ("ingredients", models.JSONField(verbose_name="Ингридиенты")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("vegan_recipe", models.BooleanField(verbose_name="Веганский рецепт")),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subscription_is_active",
                    models.BooleanField(verbose_name="Подписка"),
                ),
                (
                    "subscription_duration",
                    models.DateTimeField(verbose_name="Длительность подписки"),
                ),
                (
                    "subscription_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(max_length=20, verbose_name="Имя пользователя"),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        verbose_name="Адрес электронной почты",
                    ),
                ),
                (
                    "subscription",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_subscriptions",
                        to="recipe.subscription",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="subscription",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscriptions",
                to="recipe.user",
            ),
        ),
        migrations.CreateModel(
            name="LikeDislike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action", models.BooleanField(verbose_name="Действие пользователя")),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipe.recipe"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipe.user"
                    ),
                ),
            ],
            options={"unique_together": {("user", "recipe", "action")},},
        ),
    ]

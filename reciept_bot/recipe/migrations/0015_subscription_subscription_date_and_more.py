# Generated by Django 4.2.5 on 2023-09-20 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0014_alter_recipe_options_alter_subscription_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="subscription_date",
            field=models.DateTimeField(default=None, verbose_name="Дата подписки"),
        ),
        migrations.AlterField(
            model_name="likedislike",
            name="action",
            field=models.BooleanField(
                default=None, verbose_name="Действие пользователя"
            ),
        ),
    ]

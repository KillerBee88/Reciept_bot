# Generated by Django 4.2.5 on 2023-09-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0021_alter_subscription_subscription_duration_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription", name="subscription_duration",
        ),
        migrations.AlterField(
            model_name="subscription",
            name="subscription_date",
            field=models.DateTimeField(default=None, verbose_name="Дата подписки"),
        ),
    ]
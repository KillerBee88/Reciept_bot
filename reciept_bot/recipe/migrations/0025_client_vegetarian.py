# Generated by Django 4.2.5 on 2023-09-23 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0024_alter_subscription_subscription_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="vegetarian",
            field=models.BooleanField(default=False, verbose_name="Травоядное"),
        ),
    ]

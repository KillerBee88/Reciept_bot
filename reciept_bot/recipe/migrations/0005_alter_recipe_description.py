# Generated by Django 4.2.5 on 2023-09-19 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0004_recipe_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="description",
            field=models.CharField(
                max_length=500, verbose_name="Описание приготовления"
            ),
        ),
    ]

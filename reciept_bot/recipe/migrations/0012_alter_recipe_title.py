# Generated by Django 4.2.5 on 2023-09-19 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0011_alter_recipe_cooking_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="title",
            field=models.CharField(max_length=50, verbose_name="Название рецепта"),
        ),
    ]
# Generated by Django 4.2.5 on 2023-09-19 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0003_alter_recipe_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="description",
            field=models.CharField(
                default="a", max_length=500, verbose_name="Описание приготовления"
            ),
        ),
    ]
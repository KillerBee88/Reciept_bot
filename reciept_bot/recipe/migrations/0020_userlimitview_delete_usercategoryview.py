# Generated by Django 4.2.5 on 2023-09-21 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0019_alter_client_username"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserLimitView",
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
                ("views_left", models.IntegerField(default=3)),
                ("date", models.DateField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_views",
                        to="recipe.client",
                    ),
                ),
            ],
            options={"unique_together": {("user", "date")},},
        ),
        migrations.DeleteModel(name="UserCategoryView",),
    ]
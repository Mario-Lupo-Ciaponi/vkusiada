# Generated by Django 5.2.3 on 2025-07-24 10:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_alter_recipeingredient_recipe"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="added_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]

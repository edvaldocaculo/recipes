# Generated by Django 4.1.4 on 2023-04-14 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_category_alter_recipe_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
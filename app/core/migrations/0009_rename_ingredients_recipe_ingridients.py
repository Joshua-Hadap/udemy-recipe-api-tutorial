# Generated by Django 4.0.3 on 2022-04-10 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredients',
            new_name='ingridients',
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-11 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='desciption',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='time_minute',
            new_name='time_minutes',
        ),
    ]
# Generated by Django 5.0.4 on 2024-04-18 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_tag_recipe_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time_minutes',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

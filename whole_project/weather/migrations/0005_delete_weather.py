# Generated by Django 4.1.7 on 2023-04-03 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_remove_weather_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Weather',
        ),
    ]

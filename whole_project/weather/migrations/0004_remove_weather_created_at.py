# Generated by Django 4.1.7 on 2023-03-12 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_alter_weather_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='created_at',
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-20 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_categories_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='blog.blog'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-21 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_categories_blog_categories_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='blog',
        ),
        migrations.AddField(
            model_name='categories',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='blog.blog'),
            preserve_default=False,
        ),
    ]

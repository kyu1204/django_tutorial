# Generated by Django 3.0.4 on 2020-03-19 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200319_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='blog',
            name='published',
            field=models.DateField(auto_now=True),
        ),
    ]

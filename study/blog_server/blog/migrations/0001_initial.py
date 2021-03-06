# Generated by Django 3.0.4 on 2020-03-19 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='date published')),
                ('content', models.TextField(blank=True)),
            ],
        ),
    ]

# Generated by Django 4.1.3 on 2022-11-26 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_error'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='error',
            name='data',
        ),
    ]

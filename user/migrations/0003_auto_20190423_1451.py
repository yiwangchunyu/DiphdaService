# Generated by Django 2.2 on 2019-04-23 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190423_1442'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserOpenid',
            new_name='User',
        ),
    ]
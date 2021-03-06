# Generated by Django 2.2 on 2019-04-23 06:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserOpenid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('openid', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=1)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
                ('mtime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

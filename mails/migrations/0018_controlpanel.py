# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-11 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0017_auto_20170211_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='controlPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.IntegerField(default=0)),
                ('order', models.IntegerField(default=0)),
                ('distance', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'controlPanel',
            },
        ),
    ]

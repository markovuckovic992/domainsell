# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-10 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0005_blacklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blacklist',
            name='email',
        ),
        migrations.AddField(
            model_name='blacklist',
            name='lead',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]

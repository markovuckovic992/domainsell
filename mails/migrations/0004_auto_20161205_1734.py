# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-05 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0003_auto_20161204_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='email',
            field=models.CharField(blank=True, max_length=320, null=True),
        ),
    ]

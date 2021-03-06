# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-15 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead', models.CharField(max_length=100)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('offer_id', models.CharField(max_length=10)),
                ('base_id', models.IntegerField()),
                ('hash_base_id', models.CharField(max_length=32)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('contact', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'ponude',
            },
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 06:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('uri', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField()),
                ('headline', models.CharField(max_length=30)),
                ('news_text', models.TextField()),
                ('instrument_ids', models.TextField()),
                ('topic_codes', models.TextField()),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 03:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seng', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='query_instrument_ids',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='query_topic_codes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
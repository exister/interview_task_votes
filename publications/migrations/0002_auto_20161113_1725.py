# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rex_publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationrating',
            name='total_down_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='publicationrating',
            name='total_up_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='publicationrating',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
    ]

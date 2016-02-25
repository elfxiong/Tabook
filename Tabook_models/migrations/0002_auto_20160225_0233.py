# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tabook_models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='category',
            field=models.CharField(default='unclassified', max_length=30),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='price_range',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='table',
            name='style',
            field=models.CharField(default='unspecified', max_length=30),
        ),
        migrations.AddField(
            model_name='table',
            name='x_coordinate',
            field=models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='y_coordinate',
            field=models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True),
        ),
    ]

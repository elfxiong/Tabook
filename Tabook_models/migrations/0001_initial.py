# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('phone', models.CharField(null=True, blank=True, max_length=20)),
                ('first_name', models.CharField(null=True, blank=True, max_length=30)),
                ('last_name', models.CharField(null=True, blank=True, max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('status', models.CharField(max_length=30)),
                ('customer', models.ForeignKey(to='Tabook_models.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('phone', models.CharField(null=True, blank=True, max_length=20)),
                ('restaurant_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('price_range', models.PositiveSmallIntegerField(default=0)),
                ('category', models.CharField(default='unclassified', max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.PositiveSmallIntegerField()),
                ('style', models.CharField(default='unspecified', max_length=30)),
                ('x_coordinate', models.DecimalField(null=True, decimal_places=2, blank=True, max_digits=7)),
                ('y_coordinate', models.DecimalField(null=True, decimal_places=2, blank=True, max_digits=7)),
                ('restaurant', models.ForeignKey(to='Tabook_models.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='TableStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('available', models.BooleanField(default=False)),
                ('table', models.ForeignKey(to='Tabook_models.Table')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='table_status',
            field=models.ForeignKey(to='Tabook_models.TableStatus'),
        ),
    ]

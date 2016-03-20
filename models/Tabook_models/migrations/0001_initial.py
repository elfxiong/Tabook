# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, auto_created=True)),
                ('user_type', models.CharField(choices=[('C', 'Customer'), ('R', 'Restaurant')], max_length=2, default='C')),
                ('user_id', models.PositiveIntegerField()),
                ('token', models.CharField(primary_key=True, max_length=64, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
                ('phone', models.CharField(null=True, max_length=20, blank=True)),
                ('first_name', models.CharField(null=True, max_length=30, blank=True)),
                ('last_name', models.CharField(null=True, max_length=30, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, auto_created=True)),
                ('status', models.CharField(max_length=30)),
                ('start_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('duration', models.PositiveSmallIntegerField(default=1)),
                ('customer', models.ForeignKey(to='Tabook_models.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
                ('phone', models.CharField(null=True, max_length=20, blank=True)),
                ('restaurant_name', models.CharField(null=True, max_length=30, blank=True)),
                ('address', models.CharField(null=True, max_length=200, blank=True)),
                ('price_range', models.PositiveSmallIntegerField(null=True, blank=True, default=0)),
                ('category', models.CharField(null=True, max_length=30, blank=True, default='unclassified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RestaurantHours',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('monday_open_time', models.TimeField(default='0:00')),
                ('monday_close_time', models.TimeField(default='23:59')),
                ('tuesday_open_time', models.TimeField(default='0:00')),
                ('tuesday_close_time', models.TimeField(default='23:59')),
                ('wednesday_open_time', models.TimeField(default='0:00')),
                ('wednesday_close_time', models.TimeField(default='23:59')),
                ('thursday_open_time', models.TimeField(default='0:00')),
                ('thursday_close_time', models.TimeField(default='23:59')),
                ('friday_open_time', models.TimeField(default='0:00')),
                ('friday_close_time', models.TimeField(default='23:59')),
                ('saturday_open_time', models.TimeField(default='0:00')),
                ('saturday_close_time', models.TimeField(default='23:59')),
                ('sunday_open_time', models.TimeField(default='0:00')),
                ('sunday_close_time', models.TimeField(default='23:59')),
                ('restaurant', models.ForeignKey(to='Tabook_models.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, auto_created=True)),
                ('stars', models.PositiveSmallIntegerField(default=0)),
                ('text', models.CharField(max_length=2000)),
                ('customer', models.ForeignKey(to='Tabook_models.Customer')),
                ('restaurant', models.ForeignKey(to='Tabook_models.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('capacity', models.PositiveSmallIntegerField()),
                ('style', models.CharField(max_length=30, default='unspecified')),
                ('x_coordinate', models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7)),
                ('y_coordinate', models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7)),
                ('restaurant', models.ForeignKey(to='Tabook_models.Restaurant')),
            ],
        ),
    ]

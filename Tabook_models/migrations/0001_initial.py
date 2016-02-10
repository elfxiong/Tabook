# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('capacity', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TableStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField()),
                ('available', models.BooleanField(default=False)),
                ('table', models.ForeignKey(to='Tabook_models.Table')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='Tabook_models.User', serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
            bases=('Tabook_models.user',),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='Tabook_models.User', serialize=False, primary_key=True)),
                ('restaurant_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
            ],
            bases=('Tabook_models.user',),
        ),
        migrations.AddField(
            model_name='table',
            name='restaurant',
            field=models.ForeignKey(to='Tabook_models.Restaurant'),
        ),
    ]

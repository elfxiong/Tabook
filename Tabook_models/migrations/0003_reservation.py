# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tabook_models', '0002_auto_20160225_0233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True, auto_created=True)),
                ('status', models.CharField(max_length=30)),
                ('customer', models.ForeignKey(to='Tabook_models.Customer')),
                ('table_status', models.ForeignKey(to='Tabook_models.TableStatus')),
            ],
        ),
    ]

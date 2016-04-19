# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0003_auto_20160201_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='routerint',
            name='t_stamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 2, 7, 8, 20, 385000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='routerint',
            name='admin_up',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='routerint',
            name='protocol_up',
            field=models.CharField(max_length=20),
        ),
    ]

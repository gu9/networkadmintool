# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0004_auto_20160202_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='routeradd',
            name='user_name',
            field=models.CharField(default='gopi', max_length=32),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0002_routerint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routerint',
            name='admin_up',
            field=models.CharField(max_length=20),
        ),
    ]

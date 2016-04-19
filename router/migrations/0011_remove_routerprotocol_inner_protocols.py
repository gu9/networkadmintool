# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0010_routerprotocol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routerprotocol',
            name='inner_protocols',
        ),
    ]

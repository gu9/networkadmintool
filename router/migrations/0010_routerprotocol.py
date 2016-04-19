# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0009_routervrf_lookup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routerprotocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostip', models.CharField(max_length=32)),
                ('inner_protocols', models.CharField(max_length=200)),
                ('outer_protocols', models.CharField(max_length=200)),
            ],
        ),
    ]

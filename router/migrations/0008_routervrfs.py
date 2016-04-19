# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0007_routerpara'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routervrfs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostip', models.CharField(max_length=32)),
                ('vrf_name', models.CharField(max_length=32)),
                ('vrf_RD', models.CharField(max_length=32)),
                ('vrf_int', models.CharField(max_length=32)),
            ],
        ),
    ]

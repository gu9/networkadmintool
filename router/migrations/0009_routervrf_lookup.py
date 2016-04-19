# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0008_routervrfs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routervrf_lookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('router_id', models.CharField(max_length=50)),
                ('customer_name', models.CharField(max_length=50)),
                ('network', models.CharField(max_length=50)),
                ('protocol', models.CharField(max_length=50)),
                ('nexthop', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]

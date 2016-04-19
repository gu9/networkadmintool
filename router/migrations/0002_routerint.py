# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routerint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostip', models.CharField(max_length=32)),
                ('interface_name', models.CharField(max_length=32)),
                ('ip_addr', models.CharField(max_length=32)),
                ('admin_up', models.CharField(max_length=10)),
                ('protocol_up', models.CharField(max_length=10)),
            ],
        ),
    ]

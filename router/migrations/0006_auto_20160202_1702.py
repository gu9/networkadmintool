# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0005_routeradd_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouterAd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=32)),
                ('host_ip', models.CharField(max_length=32)),
                ('user_name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.DeleteModel(
            name='RouterAdd',
        ),
    ]

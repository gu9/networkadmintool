# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0006_auto_20160202_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routerpara',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=32)),
                ('vendor_name', models.CharField(max_length=32)),
                ('model_name', models.CharField(max_length=32)),
                ('image_name', models.CharField(max_length=32)),
                ('version_name', models.CharField(max_length=32)),
                ('cpu_usage', models.CharField(max_length=32)),
                ('cpu_speed', models.CharField(max_length=32)),
                ('mem_tot', models.CharField(max_length=32)),
                ('mem_used', models.CharField(max_length=32)),
            ],
        ),
    ]

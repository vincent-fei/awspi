# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instances',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('InstanceID', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=30)),
                ('InstanceType', models.CharField(max_length=12)),
                ('InstanceState', models.CharField(max_length=8)),
                ('Placement', models.CharField(max_length=25)),
                ('PrivateIP', models.CharField(max_length=15)),
                ('PublicIP', models.CharField(max_length=15)),
                ('VpcID', models.CharField(max_length=12)),
                ('SubnetID', models.CharField(max_length=15)),
                ('AmiID', models.CharField(max_length=12)),
                ('LaunchTime', models.CharField(max_length=24)),
                ('VirtualizationType', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Volumes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('VolumeID', models.CharField(max_length=12)),
                ('VolumeType', models.CharField(max_length=8)),
                ('VolumeSize', models.CharField(max_length=5)),
                ('AttachState', models.CharField(max_length=5)),
                ('VolumeIOPS', models.CharField(max_length=6)),
                ('VolumeZone', models.CharField(max_length=18)),
                ('CreateTime', models.CharField(max_length=24)),
                ('Project', models.CharField(max_length=30)),
                ('InstanceID', models.CharField(max_length=10)),
                ('SnapshotID', models.CharField(max_length=10)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('code_entered', models.CharField(max_length=100)),
                ('success', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'NONE', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='DoorCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(unique=True, max_length=16, db_index=True)),
                ('start', models.DateTimeField(default=datetime.datetime.now)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='codelog',
            name='code',
            field=models.ForeignKey(blank=True, to='maypi.DoorCode', null=True),
        ),
        migrations.AddField(
            model_name='codelog',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

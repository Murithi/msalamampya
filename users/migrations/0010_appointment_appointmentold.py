# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20160218_0715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=15)),
                ('time', models.DateTimeField()),
                ('time_zone', timezone_field.fields.TimeZoneField(default=b'Africa/Nairobi')),
                ('task_id', models.CharField(max_length=50, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentOld',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstchoicedate', models.DateTimeField()),
                ('secondchoicedate', models.DateTimeField()),
                ('purposeofvisit', models.CharField(max_length=600)),
                ('patient', models.ForeignKey(to='users.UserProfile')),
            ],
        ),
    ]

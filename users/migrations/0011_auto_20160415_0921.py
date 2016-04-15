# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('users', '0010_appointment_appointmentold'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('schedule', models.CharField(max_length=96)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('facility_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='dailyschedule',
            name='doctor',
            field=models.ForeignKey(related_name='day_schedule', to='users.Doctor'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccines', '0001_initial'),
        ('users', '0007_auto_20160212_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVaccination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_at', models.DateTimeField(auto_now_add=True)),
                ('date_of_vaccine_reception', models.DateTimeField()),
                ('location_of_reception', models.CharField(max_length=150, blank=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('patient_vaccine', models.ForeignKey(to='vaccines.Vaccine')),
                ('vaccine_dose', models.ForeignKey(to='vaccines.VaccineDose')),
            ],
        ),
    ]

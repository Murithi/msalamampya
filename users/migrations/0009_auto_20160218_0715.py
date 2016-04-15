# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('users', '0008_uservaccination'),
    ]

    operations = [
        migrations.CreateModel(
            name='DependantProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profilepic', models.ImageField(height_field=b'height_field', width_field=b'width_field', null=True, upload_to=users.models.upload_location, blank=True)),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('Date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('Height', models.CharField(max_length=3)),
                ('Weight', models.CharField(max_length=3)),
                ('Gender', models.CharField(max_length=1, choices=[(b'm', b'Male'), (b'f', b'Female')])),
                ('Residence', models.CharField(max_length=200)),
                ('Phone_Number', models.CharField(max_length=10)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('Dependant', models.BooleanField(default=True)),
                ('Parent', models.ForeignKey(to='users.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='patientvaccination',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='patientvaccination',
            name='patient_vaccine',
        ),
        migrations.RemoveField(
            model_name='patientvaccination',
            name='vaccine_dose',
        ),
        migrations.DeleteModel(
            name='PatientVaccination',
        ),
    ]

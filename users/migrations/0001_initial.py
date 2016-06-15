# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models
import django.utils.timezone
from django.conf import settings
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccines', '0001_initial'),
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
            ],
        ),
        migrations.CreateModel(
            name='DailySchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('schedule', models.CharField(max_length=96)),
            ],
        ),
        migrations.CreateModel(
            name='DependantProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profilepic', models.ImageField(null=True, upload_to=users.models.upload_location, blank=True)),
                ('Date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('Height', models.CharField(max_length=3)),
                ('Weight', models.CharField(max_length=3)),
                ('Gender', models.CharField(max_length=1, choices=[(b'm', b'Male'), (b'f', b'Female')])),
                ('Residence', models.CharField(max_length=200)),
                ('Phone_Number', models.CharField(max_length=10)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('Dependant', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facility_name', models.CharField(max_length=100)),
                ('facility_location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Physician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('facility', models.ForeignKey(to='users.Facility')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profilepic', models.ImageField(null=True, upload_to=users.models.upload_location, blank=True)),
                ('Date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('Height', models.CharField(max_length=3)),
                ('Weight', models.CharField(max_length=3)),
                ('Gender', models.CharField(max_length=1, choices=[(b'm', b'Male'), (b'f', b'Female')])),
                ('Residence', models.CharField(max_length=200)),
                ('Phone_Number', models.CharField(max_length=10)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('National_ID', models.CharField(max_length=8, blank=True)),
                ('Dependant', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserVaccination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_at', models.DateTimeField(auto_now_add=True)),
                ('date_of_vaccine_reception', models.DateTimeField()),
                ('location_of_reception', models.CharField(max_length=150, blank=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('patient_vaccine', models.ManyToManyField(to='vaccines.Vaccine')),
                ('vaccine_dose', models.ManyToManyField(to='vaccines.VaccineDose')),
            ],
        ),
        migrations.AddField(
            model_name='physician',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='doctor',
            name='facility',
            field=models.ForeignKey(to='users.Facility'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dependantprofile',
            name='Parent',
            field=models.ForeignKey(to='users.UserProfile'),
        ),
        migrations.AddField(
            model_name='dailyschedule',
            name='doctor',
            field=models.ForeignKey(related_name='day_schedule', to='users.Doctor'),
        ),
        migrations.AddField(
            model_name='appointmentold',
            name='patient',
            field=models.ForeignKey(to='users.UserProfile'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ManyToManyField(to='users.Doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='facility',
            field=models.ManyToManyField(to='users.Facility'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccines', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientVaccination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_at', models.DateTimeField(auto_now_add=True)),
                ('date_of_vaccine_reception', models.DateTimeField()),
                ('location_of_reception', models.CharField(max_length=150, blank=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profilepic', models.ImageField(null=True, upload_to=b'images/')),
                ('Date_of_birth', models.DateField()),
                ('Height', models.CharField(max_length=3)),
                ('Weight', models.CharField(max_length=3)),
                ('Gender', models.CharField(max_length=1, choices=[(b'm', b'Male'), (b'f', b'Female')])),
                ('Residence', models.CharField(max_length=200)),
                ('Phone_Number', models.CharField(max_length=10)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('National_ID', models.CharField(max_length=8, blank=True)),
                ('Dependant', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='patientvaccination',
            name='patient',
            field=models.ForeignKey(to='users.UserProfile'),
        ),
        migrations.AddField(
            model_name='patientvaccination',
            name='patient_vaccine',
            field=models.ForeignKey(to='vaccines.Vaccine'),
        ),
        migrations.AddField(
            model_name='patientvaccination',
            name='vaccine_dose',
            field=models.ForeignKey(to='vaccines.VaccineDose'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SideEffectbyVaccine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sideEffectDesc', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vaccine_name', models.CharField(max_length=200)),
                ('vaccine_ID_num', models.CharField(max_length=150)),
                ('vaccine_Edition', models.CharField(max_length=150)),
                ('about_Vaccine', models.CharField(max_length=500)),
                ('child_Vaccine', models.BooleanField(default=True)),
                ('last_update', models.DateField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to=b'images/')),
                ('vaccine_Dose_Count', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VaccineDose',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vaccine_dose', models.CharField(max_length=150)),
                ('vaccine_dose_date_in_months', models.IntegerField()),
                ('available', models.BooleanField()),
                ('vaccine', models.ForeignKey(to='vaccines.Vaccine')),
            ],
        ),
        migrations.AddField(
            model_name='sideeffectbyvaccine',
            name='vaccine',
            field=models.ForeignKey(to='vaccines.Vaccine'),
        ),
    ]

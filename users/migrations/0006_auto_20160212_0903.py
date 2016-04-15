# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_userprofile_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientvaccination',
            name='patient',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

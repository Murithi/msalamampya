# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160212_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profilepic',
            field=models.ImageField(height_field=b'height_field', width_field=b'width_field', null=True, upload_to=users.models.upload_location, blank=True),
        ),
    ]

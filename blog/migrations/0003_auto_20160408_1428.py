# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160408_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 8, 14, 28, 19, 323494, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 8, 14, 28, 25, 949839, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]

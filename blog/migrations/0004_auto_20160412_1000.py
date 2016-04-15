# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160408_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='intro',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blog',
            name='subtitle',
            field=models.CharField(unique=True, max_length=500),
        ),
    ]

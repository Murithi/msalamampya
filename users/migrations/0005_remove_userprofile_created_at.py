# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160212_0629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='created_at',
        ),
    ]

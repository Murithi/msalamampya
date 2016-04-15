# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160211_1119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='Timestamp',
            new_name='created_at',
        ),
    ]

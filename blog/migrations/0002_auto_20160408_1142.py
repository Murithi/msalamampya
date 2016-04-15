# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='imagecaption',
            field=models.CharField(default='testing', unique=True, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='imagecredit',
            field=models.CharField(default='testing', unique=True, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='subtitle',
            field=models.CharField(default='testing', unique=True, max_length=100),
            preserve_default=False,
        ),
    ]

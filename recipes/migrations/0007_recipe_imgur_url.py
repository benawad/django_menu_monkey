# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20160923_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='imgur_url',
            field=models.URLField(default=''),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20160914_2302'),
        ('groceries', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grocerylist',
            name='recipes',
        ),
        migrations.AddField(
            model_name='grocerylist',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.Ingredient'),
        ),
    ]

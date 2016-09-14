# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('picture', models.ImageField(upload_to='')),
                ('instructions', models.TextField()),
                ('ingredients', models.ManyToManyField(related_name='recipe_ingredients', to='recipes.Ingredient')),
                ('owner', models.ForeignKey(related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 11:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventory_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

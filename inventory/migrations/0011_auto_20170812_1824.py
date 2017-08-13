# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 16:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_auto_20170812_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='no-img.jpg', upload_to='photos/maps/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maps', to='inventory.Inventory')),
            ],
        ),
        migrations.AlterField(
            model_name='tree',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trees', to='inventory.Inventory'),
        ),
        migrations.AlterField(
            model_name='treeimage',
            name='tree',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='inventory.Tree'),
        ),
        migrations.AlterField(
            model_name='treetrunk',
            name='tree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trunks', to='inventory.Tree'),
        ),
    ]
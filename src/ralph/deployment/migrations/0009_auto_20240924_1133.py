# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2024-09-24 11:33
from __future__ import unicode_literals

from django.db import migrations
import ralph.lib.polymorphic.fields


class Migration(migrations.Migration):
    dependencies = [
        ("deployment", "0008_auto_20240705_1210"),
    ]

    operations = [
        migrations.AlterField(
            model_name="preboot",
            name="items",
            field=ralph.lib.polymorphic.fields.PolymorphicManyToManyField(
                blank=True, to="deployment.PrebootItem", verbose_name="files"
            ),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2024-05-06 16:33
from __future__ import unicode_literals

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("assets", "0034_auto_20240304_1511"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="baseobject",
            managers=[
                ("polymorphic_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]

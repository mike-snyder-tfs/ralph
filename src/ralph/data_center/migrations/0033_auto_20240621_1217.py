# Generated by Django 2.0.13 on 2024-06-21 12:17

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations

import ralph.lib.mixins.fields


class Migration(migrations.Migration):
    dependencies = [
        ("data_center", "0032_auto_20240521_1542"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="cluster",
            managers=[
                ("polymorphic_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="database",
            managers=[
                ("polymorphic_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="datacenterasset",
            managers=[
                ("polymorphic_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="vip",
            managers=[
                ("polymorphic_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="baseobjectcluster",
            name="base_object",
            field=ralph.lib.mixins.fields.BaseObjectForeignKey(
                limit_choices_to=ralph.lib.mixins.fields.BaseObjectForeignKey.limit_choices,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clusters",
                to="assets.BaseObject",
            ),
        ),
    ]

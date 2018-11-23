# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minerals', '0004_auto_20171025_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mineral',
            name='category',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='cleavage',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='color',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='crystal_habit',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='crystal_symmetry',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='crystal_system',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='diaphaneity',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='formula',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='image_caption',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='image_filename',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='luster',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='mohs_scale_hardness',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='optical_properties',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='refractive_index',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='specific_gravity',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='streak',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='strunz_classification',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mineral',
            name='unit_cell',
            field=models.TextField(blank=True),
        ),
    ]
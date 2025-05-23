# Generated by Django 5.2 on 2025-05-14 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0005_alter_plant_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='plants.category'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='plants.location'),
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-17 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(default='khaled', on_delete=django.db.models.deletion.PROTECT, to='LittleLemonAPI.category'),
        ),
    ]

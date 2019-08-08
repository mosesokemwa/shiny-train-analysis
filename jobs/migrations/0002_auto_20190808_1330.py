# Generated by Django 2.2.4 on 2019-08-08 13:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='host',
        ),
        migrations.AddField(
            model_name='provider',
            name='hosts',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=[], size=None),
            preserve_default=False,
        ),
    ]

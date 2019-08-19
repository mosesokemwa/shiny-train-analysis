# Generated by Django 2.2.4 on 2019-08-12 20:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20190809_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblisting',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='joblisting',
            name='inserted_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='joblisting',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provider',
            name='inserted_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True),
        ),
    ]
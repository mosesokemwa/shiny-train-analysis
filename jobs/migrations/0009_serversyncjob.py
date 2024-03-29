# Generated by Django 2.2.4 on 2019-08-14 08:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_auto_20190812_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerSyncJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('inserted_at', models.DateTimeField(auto_now=True)),
                ('meta', django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True)),
                ('error', models.BooleanField(default=False)),
                ('error_message', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'server_sync_jobs',
            },
        ),
    ]

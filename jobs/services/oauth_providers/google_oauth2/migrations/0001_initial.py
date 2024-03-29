# Generated by Django 2.2.4 on 2019-09-03 17:24

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleOuth2AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('inserted_at', models.DateTimeField(auto_now=True)),
                ('meta', django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('access_token', models.TextField(unique=True)),
                ('refresh_token', models.TextField()),
                ('expires', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='google_oauth2_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'google_oauth_token',
            },
        ),
    ]

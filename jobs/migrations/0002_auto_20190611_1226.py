# Generated by Django 2.2.2 on 2019-06-11 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joblisting',
            options={'verbose_name_plural': 'JobListings'},
        ),
        migrations.AddField(
            model_name='joblisting',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provder_jobs', to='jobs.Providers'),
        ),
    ]

# Generated by Django 2.2.7 on 2019-11-20 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controllers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='controller',
            old_name='requested',
            new_name='read',
        ),
        migrations.RenameField(
            model_name='controller',
            old_name='permit_irrigation',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='controller',
            old_name='time_to_irrigate',
            new_name='timer',
        ),
    ]
# Generated by Django 2.2.7 on 2019-11-18 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controllers', '0009_controller_permit_irrigation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controller',
            name='is_active',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

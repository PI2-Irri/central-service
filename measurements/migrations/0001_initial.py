# Generated by Django 2.2.6 on 2019-10-07 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controllers', '0003_auto_20191002_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActuatorsMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_consumption', models.FloatField(default=0.0)),
                ('reservoir_level', models.FloatField(default=0.0)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controllers.Controller')),
            ],
        ),
    ]

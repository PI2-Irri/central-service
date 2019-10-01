# Generated by Django 2.2.5 on 2019-09-30 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controllers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('zip', models.CharField(max_length=8)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('precipitation', models.FloatField(default=0.0)),
                ('ambient_temperature', models.FloatField(default=0.0)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controllers.Controller')),
            ],
        ),
    ]

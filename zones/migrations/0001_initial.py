# Generated by Django 2.2.7 on 2019-11-26 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controllers', '0003_auto_20191126_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('zip', models.CharField(max_length=9)),
                ('latitude', models.FloatField(blank=True, default=0.0)),
                ('longitude', models.FloatField(blank=True, default=0.0)),
                ('location', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controllers.Controller')),
            ],
        ),
    ]

# Generated by Django 2.2.7 on 2019-11-20 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('name', models.CharField(max_length=25)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('token', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('permit_irrigation', models.BooleanField(blank=True, default=False)),
                ('requested', models.BooleanField(blank=True, default=True)),
                ('time_to_irrigate', models.IntegerField(blank=True, default=0.0)),
                ('owner', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ControllerSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controllers.Controller')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

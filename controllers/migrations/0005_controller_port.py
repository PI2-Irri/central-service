# Generated by Django 2.2.6 on 2019-10-14 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controllers', '0004_controller_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='controller',
            name='port',
            field=models.CharField(default=':3000/', max_length=6),
        ),
    ]

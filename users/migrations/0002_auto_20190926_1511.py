# Generated by Django 2.2.5 on 2019-09-26 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='registration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
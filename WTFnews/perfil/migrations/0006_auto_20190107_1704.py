# Generated by Django 2.1.5 on 2019-01-07 17:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0005_auto_20190107_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 7, 17, 4, 18, 422380, tzinfo=utc)),
        ),
    ]

# Generated by Django 2.1.4 on 2019-01-07 03:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0003_auto_20190106_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 7, 3, 1, 21, 751952, tzinfo=utc)),
        ),
    ]
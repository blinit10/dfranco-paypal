# Generated by Django 3.0.2 on 2021-04-28 19:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('godjango', '0023_auto_20210424_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despliegue',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2021, 4, 28, 15, 54, 27, 689563)),
        ),
    ]

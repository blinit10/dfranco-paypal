# Generated by Django 3.0.2 on 2021-04-08 05:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('godjango', '0007_auto_20210408_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despliegue',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2021, 4, 8, 1, 20, 18, 581174)),
        ),
    ]

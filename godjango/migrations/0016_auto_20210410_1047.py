# Generated by Django 3.0.2 on 2021-04-10 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('godjango', '0015_auto_20210408_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despliegue',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2021, 4, 10, 10, 47, 23, 136761)),
        ),
    ]

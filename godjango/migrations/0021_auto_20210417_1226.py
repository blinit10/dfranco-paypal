# Generated by Django 3.0.2 on 2021-04-17 16:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('godjango', '0020_auto_20210410_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despliegue',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2021, 4, 17, 12, 26, 53, 654191)),
        ),
    ]

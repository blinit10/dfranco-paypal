# Generated by Django 3.0.2 on 2021-04-10 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('godjango', '0016_auto_20210410_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despliegue',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2021, 4, 10, 11, 14, 59, 998401)),
        ),
    ]

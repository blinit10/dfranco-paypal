# Generated by Django 3.0.2 on 2021-04-24 17:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('godjango', '0021_auto_20210417_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despliegue',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2021, 4, 24, 13, 22, 53, 749791)),
        ),
    ]

# Generated by Django 3.0.2 on 2021-04-07 22:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionGodlango',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicializado', models.BooleanField(default=False)),
                ('has_previo', models.CharField(blank=True, default='', max_length=500, verbose_name='Hash previo')),
            ],
            options={
                'verbose_name': 'Configuración de ámbito global',
                'verbose_name_plural': '*  Configuraciones de ámbito global',
            },
        ),
        migrations.CreateModel(
            name='Despliegue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('llave', models.CharField(max_length=500)),
                ('valor', models.CharField(max_length=500)),
                ('hora', models.TimeField(default=datetime.datetime(2021, 4, 7, 18, 23, 59, 970237))),
            ],
            options={
                'verbose_name': 'Despliegue',
                'verbose_name_plural': '**  Despliegues',
            },
        ),
    ]

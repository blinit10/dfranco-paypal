# Generated by Django 3.0.2 on 2021-04-10 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0011_seccionnosotrosperks_alineacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='seccionnosotrosperks',
            name='bloque_der',
            field=models.BooleanField(default=False, verbose_name='Mostrar bloque de texto a la derecha e imagen a la izquierda'),
        ),
    ]
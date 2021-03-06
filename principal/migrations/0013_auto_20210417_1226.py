# Generated by Django 3.0.2 on 2021-04-17 16:26

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0012_seccionnosotrosperks_bloque_der'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='historias/')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título')),
                ('contenido', ckeditor.fields.RichTextField(blank=True, help_text='Opcional')),
                ('visible', models.BooleanField(default=True)),
                ('fecha', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Historia',
                'verbose_name_plural': '04 - Historias',
            },
        ),
        migrations.AlterField(
            model_name='seccionnosotrosperks',
            name='bloque_der',
            field=models.BooleanField(default=False, verbose_name='Bloque de texto a la derecha'),
        ),
    ]

# Generated by Django 3.0.2 on 2021-04-10 15:22

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secciones', '0003_auto_20210410_1122'),
        ('principal', '0009_tipo_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeccionNosotrosPerks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, help_text='Opcional', max_length=300, verbose_name='Título')),
                ('imagen', models.ImageField(blank=True, help_text='Opcional', null=True, upload_to='secciones/', verbose_name='Imagen')),
                ('contenido', ckeditor.fields.RichTextField(blank=True, help_text='Opcional', verbose_name='Contenido')),
                ('seccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloques', to='secciones.SeccionNosotros')),
            ],
            options={
                'verbose_name': 'Bloque',
                'verbose_name_plural': 'Bloques',
            },
        ),
    ]
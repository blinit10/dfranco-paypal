# Generated by Django 3.0.2 on 2021-04-07 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SeccionPrincipal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título')),
                ('subtitulo', models.CharField(max_length=255, verbose_name='Subtítulo')),
                ('imagen', models.ImageField(upload_to='secciones/')),
                ('enlace', models.CharField(choices=[('productos', 'Texto 1'), ('servicios', 'Texto 2'), ('blog', 'Texto 3'), ('contacto', 'Texto 4')], max_length=255)),
            ],
            options={
                'verbose_name': 'Sección Principal',
                'verbose_name_plural': '01 - Sección Principal',
            },
        ),
    ]
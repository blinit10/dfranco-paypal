# Generated by Django 3.0.2 on 2021-04-24 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0013_auto_20210417_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='compras',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='visitas',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='HistoriaCarrusel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('video', 'Video'), ('foto', 'Foto')], default='foto', max_length=255)),
                ('multimedia', models.FileField(upload_to='historias/multimedia/')),
                ('seccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='galeria', to='principal.Historia')),
            ],
            options={
                'verbose_name': 'Multimedia',
                'verbose_name_plural': 'Multimedias',
            },
        ),
    ]

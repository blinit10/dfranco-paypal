# Generated by Django 3.0.2 on 2021-04-08 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_galeriaproducto_product_productoperks'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tipo',
            field=models.CharField(choices=[('Servicio', 'Servicio'), ('Producto', 'Producto')], default='Servicio', max_length=255),
            preserve_default=False,
        ),
    ]

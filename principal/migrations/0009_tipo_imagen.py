# Generated by Django 3.0.2 on 2021-04-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0008_auto_20210408_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipo',
            name='imagen',
            field=models.ImageField(default='a.jpg', upload_to='tipos'),
            preserve_default=False,
        ),
    ]

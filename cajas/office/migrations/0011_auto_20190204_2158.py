# Generated by Django 2.0.9 on 2019-02-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0010_auto_20190204_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='consecutive',
            field=models.IntegerField(default=0, verbose_name='Consecutivo Socios'),
        ),
        migrations.AlterField(
            model_name='office',
            name='number',
            field=models.IntegerField(default=1, verbose_name='Número de la oficina'),
        ),
    ]

# Generated by Django 2.0.9 on 2019-01-18 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boxcountry',
            options={'verbose_name': 'Caja de País', 'verbose_name_plural': 'Cajas de Paises'},
        ),
        migrations.AlterModelOptions(
            name='boxdailysquare',
            options={'verbose_name': 'Caja de Cuadre Diario', 'verbose_name_plural': 'Cajas de Cuadre Diario'},
        ),
    ]

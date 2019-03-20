# Generated by Django 2.0.9 on 2019-01-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0002_auto_20181221_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='concept_type',
            field=models.CharField(choices=[('SM', 'Simple'), ('DB', 'Doble partida'), ('SD', 'Simple y Doble Partida')], max_length=5, verbose_name='Tipo de concepto'),
        ),
    ]
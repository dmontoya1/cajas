# Generated by Django 2.0.9 on 2019-01-28 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0004_auto_20190118_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='concept',
            name='movement_type',
            field=models.BooleanField(default=True, help_text='Indicar si el movimiento genera o no un movimiento en las cajas. Como el caso de ENTREGA DE DINERO. Éste no génera movimiento en la caja', verbose_name='El concepto genera movimiento en la caja?'),
        ),
    ]
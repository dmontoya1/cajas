# Generated by Django 2.0.9 on 2019-03-26 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0003_movementrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movementrequest',
            options={'verbose_name': 'Requerimiento de Movimiento', 'verbose_name_plural': 'Requerimientos de movimientos'},
        ),
    ]

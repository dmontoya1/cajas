# Generated by Django 2.0.9 on 2019-07-19 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0011_auto_20190521_1454'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movementbetweenofficerequest',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Requerimiento de Movimiento entre oficinas', 'verbose_name_plural': 'Requerimientos de Movimientos entre oficinas'},
        ),
        migrations.AlterModelOptions(
            name='movementboxcolombia',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Movimiento de la caja de Colombia', 'verbose_name_plural': 'Movimientos de la caja de Colombia'},
        ),
        migrations.AlterModelOptions(
            name='movementdailysquare',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Movimiento del Cuadre Diario', 'verbose_name_plural': 'Movimientos del Cuadre Diario'},
        ),
        migrations.AlterModelOptions(
            name='movementdonjuan',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Movimiento de Don Juan', 'verbose_name_plural': 'Movimientos de Don Juan'},
        ),
        migrations.AlterModelOptions(
            name='movementdonjuanusd',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Movimiento de Don Juan', 'verbose_name_plural': 'Movimientos de Don Juan'},
        ),
        migrations.AlterModelOptions(
            name='movementoffice',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Movimiento de la oficina', 'verbose_name_plural': 'Movimientos de la oficina'},
        ),
        migrations.AlterModelOptions(
            name='movementpartner',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Movimiento del socio', 'verbose_name_plural': 'Movimientos del socio'},
        ),
        migrations.AlterModelOptions(
            name='movementprovisioning',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Movimiento de aprovisionamiento', 'verbose_name_plural': 'Movimientos de aprovisionamiento'},
        ),
        migrations.AlterModelOptions(
            name='movementrequest',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Requerimiento de Movimiento', 'verbose_name_plural': 'Requerimientos de movimientos'},
        ),
        migrations.AlterModelOptions(
            name='movementwithdraw',
            options={'ordering': ['-date', '-pk'], 'verbose_name': 'Requerimiento de retiro', 'verbose_name_plural': 'Requerimientos de retiro'},
        ),
        migrations.AlterField(
            model_name='movementbetweenofficerequest',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementboxcolombia',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementdailysquare',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementdonjuan',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementdonjuanusd',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementoffice',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementpartner',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementprovisioning',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementrequest',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
        migrations.AlterField(
            model_name='movementwithdraw',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo a la fecha'),
        ),
    ]

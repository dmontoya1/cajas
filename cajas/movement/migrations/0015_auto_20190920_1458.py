# Generated by Django 2.0.9 on 2019-09-20 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0014_auto_20190920_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movementoffice',
            name='movement_office',
        ),
        migrations.AddField(
            model_name='movementoffice',
            name='movement_colombia',
            field=models.IntegerField(blank=True, null=True, verbose_name='Movimiento Oficina Colombia PK'),
        ),
        migrations.AlterField(
            model_name='movementboxcolombia',
            name='movement_don_juan_usd',
            field=models.IntegerField(blank=True, null=True, verbose_name='Movimiento Don Juan Dólares PK'),
        ),
        migrations.AlterField(
            model_name='movementdonjuan',
            name='movement_don_juan_usd',
            field=models.IntegerField(blank=True, null=True, verbose_name='Movimiento Don Juan Dólares PK'),
        ),
        migrations.AlterField(
            model_name='movementoffice',
            name='movement_don_juan_usd',
            field=models.IntegerField(blank=True, null=True, verbose_name='Movimiento Don Juan Dólares PK'),
        ),
    ]
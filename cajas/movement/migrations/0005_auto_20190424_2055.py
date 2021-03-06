# Generated by Django 2.0.9 on 2019-04-24 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0004_auto_20190423_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementdailysquare',
            name='movement_cd',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movement.MovementDailySquare', verbose_name='Movimiento CD Contrapartida'),
        ),
        migrations.AlterField(
            model_name='movementdailysquare',
            name='movement_don_juan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movement.MovementDonJuan', verbose_name='Movimiento Don Juan Contrapartida'),
        ),
        migrations.AlterField(
            model_name='movementdailysquare',
            name='movement_don_juan_usd',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movement.MovementDonJuanUsd', verbose_name='Movimiento Don Juan Dolares Contrapartida'),
        ),
        migrations.AlterField(
            model_name='movementdailysquare',
            name='movement_office',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movement.MovementOffice', verbose_name='Movimiento Oficina Contrapartida'),
        ),
        migrations.AlterField(
            model_name='movementdailysquare',
            name='movement_partner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movement.MovementPartner', verbose_name='Movimiento Socio Contrapartida'),
        ),
    ]

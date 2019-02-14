# Generated by Django 2.0.9 on 2019-02-11 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boxes', '0010_boxdonjuan'),
        ('concepts', '0007_auto_20190204_1526'),
        ('movement', '0006_auto_20190204_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovementDonJuan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('IN', 'Entra'), ('OUT', 'Sale')], max_length=10, verbose_name='Tipo de movimiento')),
                ('value', models.IntegerField(default=0, verbose_name='Valor')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='Detalle')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='Dirección IP responsable')),
                ('balance', models.IntegerField(default=0, verbose_name='Saldo')),
                ('box_don_juan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movements', to='boxes.BoxDonJuan', verbose_name='Caja Don Juan Oficina')),
                ('concept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='concepts.Concept', verbose_name='Concepto')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Responsable')),
            ],
            options={
                'verbose_name': 'Movimiento de Don Juan',
                'verbose_name_plural': 'Movimientos de Don Juan',
            },
        ),
    ]

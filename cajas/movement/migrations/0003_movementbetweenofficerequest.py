# Generated by Django 2.0.9 on 2019-04-20 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0006_boxpartner_box_status'),
        ('concepts', '0002_auto_20190408_1614'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movement', '0002_auto_20190408_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovementBetweenOfficeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('IN', 'Entra'), ('OUT', 'Sale')], max_length=10, verbose_name='Tipo de movimiento')),
                ('value', models.IntegerField(default=0, verbose_name='Valor')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='Detalle')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='Dirección IP responsable')),
                ('balance', models.IntegerField(default=0, verbose_name='Saldo')),
                ('observation', models.TextField(help_text='Observación por la cual se debería de aceptar el movimiento', verbose_name='Observación')),
                ('box_office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movements_between_office', to='boxes.BoxOffice', verbose_name='Caja oficina')),
                ('concept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='concepts.Concept', verbose_name='Concepto')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Responsable')),
            ],
            options={
                'verbose_name': 'Requerimiento de Movimiento entre oficinas',
                'verbose_name_plural': 'Requerimientos de Movimientos entre oficinas',
            },
        ),
    ]

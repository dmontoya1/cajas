# Generated by Django 2.0.9 on 2019-02-11 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20190211_1602'),
        ('office', '0012_auto_20190204_2210'),
        ('boxes', '0009_auto_20190204_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxDonJuan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0, verbose_name='Saldo de la caja')),
                ('is_active', models.BooleanField(default=True, verbose_name='Caja Activa?')),
                ('last_movement_id', models.IntegerField(default=0, verbose_name='id último movimiento')),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='office.Office', verbose_name='Oficina')),
                ('partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Partner', verbose_name='Don Juan')),
            ],
            options={
                'verbose_name': 'Caja de Don Juan',
                'verbose_name_plural': 'Cajas de Don Juan',
            },
        ),
    ]
# Generated by Django 2.0.9 on 2019-03-20 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre Cadena')),
                ('places', models.IntegerField(default=1, verbose_name='Número de puestos')),
                ('place_value', models.FloatField(default=0, verbose_name='Precio por puesto')),
                ('chain_type', models.CharField(choices=[('IN', 'Interna'), ('EX', 'Externa')], default='IN', max_length=2, verbose_name='Tipo de cadena')),
            ],
            options={
                'verbose_name': 'Cadena',
            },
        ),
        migrations.CreateModel(
            name='ChainPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Número de puesto')),
                ('pay_date', models.DateField(verbose_name='Fecha de pago del puesto')),
            ],
            options={
                'verbose_name': 'Puesto de la cadena',
                'verbose_name_plural': 'Puestos de la cadena',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_porcentaje', models.FloatField(verbose_name='Porcentaje del usuario')),
                ('chain_place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_users', to='chains.ChainPlace', verbose_name='Puesto de la cadena')),
            ],
            options={
                'verbose_name': 'Usuario por puesto',
                'verbose_name_plural': 'Usuarios por puesto',
                'ordering': ['id'],
            },
        ),
    ]

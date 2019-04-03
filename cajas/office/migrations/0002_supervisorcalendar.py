# Generated by Django 2.0.9 on 2019-04-01 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0003_unit_observations'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisorCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField(auto_now=True, verbose_name='Fecha de calendario de supervisor')),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_supervisor_calendar', to='office.Office', verbose_name='Oficina')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_supervisor_calendar', to=settings.AUTH_USER_MODEL, verbose_name='Supervisor')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.Unit', verbose_name='Unidad')),
            ],
            options={
                'verbose_name': 'Calendario de supervisor',
                'verbose_name_plural': 'Calendarios de supervisores',
            },
        ),
    ]
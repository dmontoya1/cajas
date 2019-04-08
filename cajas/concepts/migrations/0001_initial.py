# Generated by Django 2.0.9 on 2019-04-08 16:14

import concepts.models.concepts
from django.db import migrations, models
import enumfields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('concept_type', enumfields.fields.EnumField(enum=concepts.models.concepts.ConceptType, max_length=2, verbose_name='Tipo de concepto')),
                ('crossover_type', enumfields.fields.EnumField(blank=True, enum=concepts.models.concepts.CrossoverType, max_length=2, null=True, verbose_name='Tipo de cruce')),
                ('relationship', enumfields.fields.EnumField(blank=True, enum=concepts.models.concepts.Relationship, max_length=7, null=True, verbose_name='Relación del movimiento')),
                ('movement_type', models.BooleanField(default=True, help_text='Indicar si el movimiento genera o no un movimiento en las cajas. Como el caso de ENTREGA DE DINERO. Éste no génera movimiento en la caja', verbose_name='El concepto genera movimiento en la caja?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Concepto activo?')),
            ],
            options={
                'verbose_name': 'Concepto',
            },
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(verbose_name='Valor del tope')),
            ],
            options={
                'verbose_name': 'Tope',
            },
        ),
    ]

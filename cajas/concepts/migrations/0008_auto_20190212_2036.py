# Generated by Django 2.0.9 on 2019-02-12 20:36

import concepts.models.concepts
from django.db import migrations
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0007_auto_20190204_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='concept_type',
            field=enumfields.fields.EnumField(enum=concepts.models.concepts.ConceptType, max_length=2),
        ),
        migrations.AlterField(
            model_name='concept',
            name='crossover_type',
            field=enumfields.fields.EnumField(blank=True, enum=concepts.models.concepts.CrossoverType, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='concept',
            name='relationship',
            field=enumfields.fields.EnumField(blank=True, enum=concepts.models.concepts.Relationship, max_length=7, null=True),
        ),
    ]

# Generated by Django 2.0.9 on 2018-12-19 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nombre de la marca. Ejm: Samsung, Honda, HP, ... etc.', max_length=255, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Marca',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nombre de la categoria. Ejm: Celulares, motos, equipo de oficina, computadores...etc.', max_length=255, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_brands', to='inventory.Category', verbose_name='Categoria'),
        ),
    ]

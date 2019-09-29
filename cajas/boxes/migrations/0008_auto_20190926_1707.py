# Generated by Django 2.0.9 on 2019-09-26 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0007_boxcolombia'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boxdonjuan',
            options={'verbose_name': 'Caja del Presidente', 'verbose_name_plural': 'Cajas del Presidente'},
        ),
        migrations.AlterModelOptions(
            name='boxdonjuanusd',
            options={'verbose_name': 'Caja de oficina Dolares', 'verbose_name_plural': 'Cajas de oficina Dolares'},
        ),
        migrations.AlterField(
            model_name='boxdonjuan',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Partner', verbose_name='Presidente'),
        ),
        migrations.AlterField(
            model_name='boxdonjuanusd',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Partner', verbose_name='Presidente'),
        ),
    ]
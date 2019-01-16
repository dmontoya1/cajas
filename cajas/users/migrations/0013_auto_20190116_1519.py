# Generated by Django 2.0.9 on 2019-01-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20181221_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='partner_type',
            field=models.CharField(choices=[('DIR', 'Directo'), ('INDIR', 'Indirecto'), ('DJ', 'Don Juan')], max_length=10, verbose_name='Tipo de socio'),
        ),
    ]

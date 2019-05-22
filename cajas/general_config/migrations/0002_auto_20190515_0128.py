# Generated by Django 2.0.9 on 2019-05-15 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='exchange_cop',
            field=models.FloatField(help_text='Factor de cambio para prestamos, abonos e intereses de la divisa a peso colombiano', verbose_name='Factor divisa a Peso Colombiano'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='exchange_dolar',
            field=models.FloatField(help_text='Tasa de cambio para prestamos, abonos e intereses de la divisa a dolar', verbose_name='Cambio divisa a Dolar'),
        ),
    ]

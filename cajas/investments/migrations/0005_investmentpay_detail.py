# Generated by Django 2.0.9 on 2019-04-04 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0004_auto_20190404_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentpay',
            name='detail',
            field=models.TextField(default='', verbose_name='Detalle del pago'),
        ),
    ]
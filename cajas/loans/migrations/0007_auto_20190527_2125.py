# Generated by Django 2.0.9 on 2019-05-27 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0006_auto_20190520_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='balance_cop',
            field=models.FloatField(default=0, verbose_name='Saldo a la fecha (En COP)'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_provider_loan', to='users.Partner', verbose_name='Fondeador'),
        ),
    ]
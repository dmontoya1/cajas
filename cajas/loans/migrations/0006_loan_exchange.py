# Generated by Django 2.0.9 on 2019-03-06 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0005_auto_20190306_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='exchange',
            field=models.FloatField(default=0, verbose_name='Tasa de cambio'),
        ),
    ]
# Generated by Django 2.0.9 on 2019-01-30 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0003_auto_20190128_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementcountry',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo'),
        ),
        migrations.AddField(
            model_name='movementdailysquare',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo'),
        ),
        migrations.AddField(
            model_name='movementoffice',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo'),
        ),
        migrations.AddField(
            model_name='movementpartner',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Saldo'),
        ),
    ]
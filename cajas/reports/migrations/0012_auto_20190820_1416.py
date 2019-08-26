# Generated by Django 2.0.9 on 2019-08-20 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_auto_20190801_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankingoffice',
            name='end_date',
            field=models.DateField(default=datetime.date(2019, 8, 20), verbose_name='Fecha fin ranking'),
        ),
        migrations.AlterField(
            model_name='rankingoffice',
            name='start_date',
            field=models.DateField(default=datetime.date(2019, 8, 20), verbose_name='Fecha inicio ranking'),
        ),
    ]

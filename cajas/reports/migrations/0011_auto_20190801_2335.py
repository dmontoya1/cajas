# Generated by Django 2.0.9 on 2019-08-01 23:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_auto_20190725_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankingoffice',
            name='end_date',
            field=models.DateField(default=datetime.date(2019, 8, 1), verbose_name='Fecha fin ranking'),
        ),
        migrations.AlterField(
            model_name='rankingoffice',
            name='start_date',
            field=models.DateField(default=datetime.date(2019, 8, 1), verbose_name='Fecha inicio ranking'),
        ),
    ]

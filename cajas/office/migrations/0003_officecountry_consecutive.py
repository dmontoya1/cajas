# Generated by Django 2.0.9 on 2019-04-09 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0002_auto_20190408_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='officecountry',
            name='consecutive',
            field=models.IntegerField(default=1, verbose_name='Consecutivo Socios'),
        ),
    ]

# Generated by Django 2.0.9 on 2019-05-29 15:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0006_auto_20190528_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='report_users',
            field=models.ManyToManyField(related_name='related_users_report', to=settings.AUTH_USER_MODEL, verbose_name='Informar usuarios'),
        ),
    ]
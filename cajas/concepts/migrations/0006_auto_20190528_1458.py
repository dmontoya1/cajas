# Generated by Django 2.0.9 on 2019-05-28 14:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0005_auto_20190513_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='report_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='related_users_report', to=settings.AUTH_USER_MODEL, verbose_name='Informar usuarios'),
        ),
    ]

# Generated by Django 2.0.9 on 2019-04-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0006_auto_20190426_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisorcalendar',
            name='detail',
            field=models.TextField(default='', verbose_name='Detalle del agendamiento'),
        ),
    ]

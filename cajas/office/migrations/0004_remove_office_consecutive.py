# Generated by Django 2.0.9 on 2019-04-09 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0003_officecountry_consecutive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='office',
            name='consecutive',
        ),
    ]

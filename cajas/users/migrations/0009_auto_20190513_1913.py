# Generated by Django 2.0.9 on 2019-05-13 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190422_2016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['user__first_name'], 'verbose_name': 'Socio', 'verbose_name_plural': 'Socios'},
        ),
    ]

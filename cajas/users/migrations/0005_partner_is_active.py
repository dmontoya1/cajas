# Generated by Django 2.0.9 on 2019-04-15 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190408_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Socio activo?'),
        ),
    ]

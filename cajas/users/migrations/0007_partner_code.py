# Generated by Django 2.0.9 on 2018-12-18 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='code',
            field=models.CharField(default='code', max_length=255, verbose_name='Código'),
            preserve_default=False,
        ),
    ]
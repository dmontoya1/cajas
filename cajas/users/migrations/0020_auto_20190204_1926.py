# Generated by Django 2.0.9 on 2019-02-04 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_user_is_daily_square'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_daily_square',
        ),
        migrations.AddField(
            model_name='employee',
            name='is_daily_square',
            field=models.BooleanField(default=False, verbose_name='Es cuadre diarioo?'),
        ),
        migrations.AddField(
            model_name='partner',
            name='is_daily_square',
            field=models.BooleanField(default=False, verbose_name='Es cuadre diarioo?'),
        ),
    ]
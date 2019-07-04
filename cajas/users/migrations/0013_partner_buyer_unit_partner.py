# Generated by Django 2.0.9 on 2019-07-03 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190611_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='buyer_unit_partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_unit_buyer', to='users.Partner', verbose_name='Socio al que se le vendio la ultima unidad'),
        ),
    ]
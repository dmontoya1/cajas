# Generated by Django 2.0.9 on 2019-01-25 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general_config', '0003_auto_20190125_1556'),
        ('boxes', '0002_auto_20190118_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxcountry',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='general_config.Currency', verbose_name='Divisa de la caja'),
        ),
    ]

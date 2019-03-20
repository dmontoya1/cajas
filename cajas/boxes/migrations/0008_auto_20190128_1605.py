# Generated by Django 2.0.9 on 2019-01-28 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0007_auto_20190128_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxoffice',
            name='office',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='box', to='office.Office', verbose_name='Oficina'),
        ),
    ]
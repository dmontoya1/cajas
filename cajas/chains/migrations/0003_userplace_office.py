# Generated by Django 2.0.9 on 2019-09-19 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0008_auto_20190502_1343'),
        ('chains', '0002_auto_20190408_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplace',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_places', to='office.OfficeCountry', verbose_name='Oficina a la que pertenece el usuario'),
        ),
    ]

# Generated by Django 2.0.9 on 2019-04-08 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='office',
            field=models.ManyToManyField(blank=True, related_name='related_employees', to='office.Office', verbose_name='Oficina'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='office_country',
            field=models.ManyToManyField(blank=True, related_name='related_employees', to='office.OfficeCountry', verbose_name='Oficina por País'),
        ),
    ]

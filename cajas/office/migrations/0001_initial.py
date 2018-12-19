# Generated by Django 2.0.9 on 2018-12-19 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_config', '0002_country_abbr'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Telefono')),
                ('address', models.CharField(max_length=255, verbose_name='Direccion')),
                ('admin_junior', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_junior_office', to=settings.AUTH_USER_MODEL, verbose_name='Adminsitrador Junior')),
                ('admin_senior', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_senior_office', to=settings.AUTH_USER_MODEL, verbose_name='Adminsitrador Senior')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general_config.Country', verbose_name='Pais')),
                ('secretary', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_secretary_office', to=settings.AUTH_USER_MODEL, verbose_name='Secretaria')),
            ],
            options={
                'verbose_name': 'Oficina',
                'verbose_name_plural': 'Oficinas',
            },
        ),
    ]
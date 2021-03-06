# Generated by Django 2.0.9 on 2019-04-08 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('office', '0001_initial'),
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='lender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_lender_user', to=settings.AUTH_USER_MODEL, verbose_name='Deudor'),
        ),
        migrations.AddField(
            model_name='loan',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='office.OfficeCountry', verbose_name='Oficina'),
        ),
        migrations.AddField(
            model_name='loan',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_provider_loan', to=settings.AUTH_USER_MODEL, verbose_name='Fondeador'),
        ),
    ]

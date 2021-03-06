# Generated by Django 2.0.9 on 2019-04-08 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('office', '0001_initial'),
        ('chains', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplace',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_chains', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='chainplace',
            name='chain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_places', to='chains.Chain', verbose_name='Cadena'),
        ),
        migrations.AddField(
            model_name='chain',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_chaines', to='office.OfficeCountry', verbose_name='Oficina'),
        ),
    ]

# Generated by Django 2.0.9 on 2019-04-08 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('boxes', '0002_boxprovisioning_office'),
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxpartner',
            name='partner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='box', to='users.Partner', verbose_name='Socio'),
        ),
        migrations.AddField(
            model_name='boxoffice',
            name='office',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='box', to='office.OfficeCountry', verbose_name='Oficina del País'),
        ),
        migrations.AddField(
            model_name='boxdonjuanusd',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='office.OfficeCountry', verbose_name='Oficina por país'),
        ),
        migrations.AddField(
            model_name='boxdonjuanusd',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Partner', verbose_name='Don Juan'),
        ),
        migrations.AddField(
            model_name='boxdonjuan',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='office.OfficeCountry', verbose_name='Oficina por país'),
        ),
        migrations.AddField(
            model_name='boxdonjuan',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Partner', verbose_name='Don Juan'),
        ),
        migrations.AddField(
            model_name='boxdailysquare',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_daily_square_boxes', to='office.OfficeCountry', verbose_name='Oficina'),
        ),
        migrations.AddField(
            model_name='boxdailysquare',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_daily_box', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]

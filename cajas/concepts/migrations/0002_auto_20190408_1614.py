# Generated by Django 2.0.9 on 2019-04-08 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('concepts', '0001_initial'),
        ('general_config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stop',
            name='charge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Charge', verbose_name='Cargo'),
        ),
        migrations.AddField(
            model_name='stop',
            name='concept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concepts.Concept', verbose_name='Concepto'),
        ),
        migrations.AddField(
            model_name='stop',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general_config.Country', verbose_name='Pais'),
        ),
        migrations.AddField(
            model_name='stop',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Socio, empleado'),
        ),
        migrations.AddField(
            model_name='concept',
            name='counterpart',
            field=models.ForeignKey(blank=True, help_text='Concepto de contrapartida cuando el concepto es de cruce.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='concepts.Concept', verbose_name='Concepto Contrapartida'),
        ),
    ]

# Generated by Django 2.0.9 on 2019-03-27 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0005_movementprovisioning'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementrequest',
            name='withdraw_reason',
            field=models.TextField(blank=True, null=True, verbose_name='Razón de solicitud de permiso retiro de socio'),
        ),
    ]
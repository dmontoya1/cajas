# Generated by Django 2.0.9 on 2019-05-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0010_movementbetweenofficerequest_origin_office'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementbetweenofficerequest',
            name='from_box_type',
            field=models.CharField(choices=[('BDJ', 'Caja de Don Juan'), ('BCO', 'Caja Colombia')], default='BDJ', max_length=3, verbose_name='Origen del movimiento'),
        ),
        migrations.AddField(
            model_name='movementbetweenofficerequest',
            name='origin_movement_pk',
            field=models.IntegerField(blank=True, null=True, verbose_name='PK movimiento origen'),
        ),
    ]

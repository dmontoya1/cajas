# Generated by Django 2.0.9 on 2018-12-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='document_id',
            field=models.CharField(default=1, max_length=15, unique=True, verbose_name='Número Documento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='document_type',
            field=models.CharField(choices=[('CC', 'Cédula de ciudadania'), ('CE', 'Cédula de extranjería'), ('PA', 'Pasaporte')], default='1', max_length=3, verbose_name='Tipo Documento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_abstract',
            field=models.BooleanField(default=True, verbose_name='Es abstracto?'),
        ),
    ]
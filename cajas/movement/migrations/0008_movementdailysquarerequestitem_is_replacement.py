# Generated by Django 2.0.9 on 2019-04-27 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0007_auto_20190426_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementdailysquarerequestitem',
            name='is_replacement',
            field=models.BooleanField(default=False, verbose_name='Item de repuesto?'),
        ),
    ]
# Generated by Django 2.0.9 on 2019-09-20 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movement', '0015_auto_20190920_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movementoffice',
            old_name='movement_colombia',
            new_name='movement_box_colombia',
        ),
    ]
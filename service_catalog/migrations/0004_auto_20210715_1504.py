# Generated by Django 3.1.7 on 2021-07-15 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0003_auto_20210518_1513'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jobtemplate',
            unique_together={('tower_id', 'tower_server')},
        ),
    ]
# Generated by Django 3.1.7 on 2021-03-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0002_operation_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
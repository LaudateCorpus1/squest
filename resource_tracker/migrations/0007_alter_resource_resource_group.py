# Generated by Django 3.2.7 on 2021-11-16 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource_tracker', '0006_auto_20211105_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='resource_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resources', related_query_name='resource', to='resource_tracker.resourcegroup'),
        ),
    ]

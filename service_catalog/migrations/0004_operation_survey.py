# Generated by Django 3.1.7 on 2021-03-11 13:31

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0003_auto_20210309_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='survey',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
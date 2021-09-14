# Generated by Django 3.1.7 on 2021-09-09 14:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billinggroup',
            name='user_set',
            field=models.ManyToManyField(blank=True, help_text='The users in this billing group.',
                                         related_name='billing_groups', related_query_name='billing_groups',
                                         to=settings.AUTH_USER_MODEL, verbose_name='billing groups'),
        ),
    ]
# Generated by Django 2.2.6 on 2019-10-22 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='mobile',
        ),
    ]

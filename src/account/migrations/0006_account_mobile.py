# Generated by Django 2.2.6 on 2019-10-22 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_account_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='mobile',
            field=models.CharField(default=False, max_length=30),
        ),
    ]

# Generated by Django 2.2.6 on 2019-10-22 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='mobile',
            field=models.CharField(default=True, max_length=12, unique=True),
        ),
    ]

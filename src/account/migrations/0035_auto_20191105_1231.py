# Generated by Django 2.2.6 on 2019-11-05 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_auto_20191105_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]

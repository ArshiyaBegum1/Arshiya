# Generated by Django 2.2.6 on 2019-11-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0038_auto_20191105_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_freelancer',
            field=models.IntegerField(default=False),
        ),
    ]

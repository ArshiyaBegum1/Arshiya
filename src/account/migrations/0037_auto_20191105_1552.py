# Generated by Django 2.2.6 on 2019-11-05 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0036_auto_20191105_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]

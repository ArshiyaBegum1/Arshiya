# Generated by Django 2.2.6 on 2019-10-30 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20191029_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kycinfo',
            name='username',
        ),
    ]
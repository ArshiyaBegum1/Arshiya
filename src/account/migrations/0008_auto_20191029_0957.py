# Generated by Django 2.2.6 on 2019-10-29 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_kycinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kycinfo',
            name='idproofback',
        ),
        migrations.RemoveField(
            model_name='kycinfo',
            name='idprooffront',
        ),
    ]
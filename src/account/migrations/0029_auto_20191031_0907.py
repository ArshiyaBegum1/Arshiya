# Generated by Django 2.2.6 on 2019-10-31 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_auto_20191031_0646'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('files', models.FileField(upload_to='pictures/files/')),
                ('userid', models.IntegerField(default=None, null=True)),
                ('username', models.CharField(default=None, max_length=50, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ProjectInfo',
        ),
    ]
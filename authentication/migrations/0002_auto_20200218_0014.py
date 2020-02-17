# Generated by Django 2.2.5 on 2020-02-17 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='hash',
            field=models.UUIDField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='address2',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(default=None, max_length=100),
        ),
    ]

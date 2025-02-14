# Generated by Django 2.2.5 on 2020-02-19 16:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email_sent',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='verification_token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]

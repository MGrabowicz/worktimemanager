# Generated by Django 3.2.9 on 2022-02-03 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_group_isemailverified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='isEmailVerified',
        ),
        migrations.AddField(
            model_name='wtmuser',
            name='isEmailVerified',
            field=models.BooleanField(default=False),
        ),
    ]

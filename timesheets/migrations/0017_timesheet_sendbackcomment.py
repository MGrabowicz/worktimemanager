# Generated by Django 3.2.9 on 2022-03-01 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0016_auto_20220228_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='sendBackComment',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]

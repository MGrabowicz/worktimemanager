# Generated by Django 3.2.9 on 2022-02-28 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0011_rename_totalworkhours_timesheet_totalworkminutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='sentBackForChange',
            field=models.BooleanField(default=False),
        ),
    ]

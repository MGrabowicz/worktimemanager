# Generated by Django 3.2.9 on 2022-02-26 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0010_timesheet_totalworkhours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timesheet',
            old_name='totalWorkHours',
            new_name='totalWorkMinutes',
        ),
    ]

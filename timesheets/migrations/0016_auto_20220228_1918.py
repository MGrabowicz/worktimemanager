# Generated by Django 3.2.9 on 2022-02-28 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0015_alter_timesheet_timesheetstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='sentBackForChange',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='sentToAccept',
        ),
    ]

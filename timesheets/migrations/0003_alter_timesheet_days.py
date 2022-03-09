# Generated by Django 3.2.9 on 2022-02-16 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0002_alter_timesheetday_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='days',
            field=models.ManyToManyField(blank=True, default=None, related_name='days', to='timesheets.TimesheetDay'),
        ),
    ]

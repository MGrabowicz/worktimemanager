from django.contrib import admin

from timesheets.models import TimesheetDay, Timesheet

admin.site.register(TimesheetDay)
admin.site.register(Timesheet)

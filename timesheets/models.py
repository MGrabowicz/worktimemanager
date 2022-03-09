import datetime

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class TimesheetDay(models.Model):
    date = models.DateField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', default=None, blank=True,
                              on_delete=models.CASCADE)
    startTime = models.TimeField(auto_now=False, auto_now_add=False, default='00:00')
    endTime = models.TimeField(auto_now=False, auto_now_add=False, default='00:00')
    breakTime = models.TimeField(auto_now=False, auto_now_add=False, default='00:00')
    workTime = models.TimeField(auto_now=False, auto_now_add=False, default='00:00')

    def __str__(self):
        self.objectName = str(self.owner.username) + str(self.date)
        return self.objectName


class Timesheet(models.Model):
    class TimesheetStatus(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        SENTTOAPPROVE = 'SENTTOAPPROVE', _('Sent to approve')
        SENTBACKFORCHANGE = 'SENTBACKFORCHANGE', _('Sent back for change')
        APPROVED = 'APPROVED', _('Approved')

    days = models.ManyToManyField(TimesheetDay, related_name='days', default=None, blank=True)
    month = models.CharField(default=None, blank=True, null=True, max_length=20)
    monthNumber = models.IntegerField(default=1, blank=True, null=True)
    year = models.IntegerField(default=None, blank=True, null=True)
    managerToAccept = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='managerToAccept', default=None,
                                        blank=True, on_delete=models.CASCADE)
    timesheetOwner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='timesheetOwner', default=None,
                                       blank=True, on_delete=models.CASCADE)
    totalWorkMinutes = models.IntegerField(default=0, null=True)
    sendBackComment = models.TextField(default='', blank=True, null=True)
    timesheetStatus = models.CharField(
        max_length=17,
        choices=TimesheetStatus.choices,
        default=TimesheetStatus.CREATED,
    )

    def __str__(self):
        self.objectName = str(self.timesheetOwner.username) + str(self.month) + str(self.year)
        return self.objectName

    def getTimesheetObjectForTemplate(self):
        timesheetObject = []
        for day in self.days.all().order_by('date'):
            timesheetObject.append({
                'fullDate': day.date.strftime("%d %B, %Y").title(),
                'dayOfWeek': day.date.strftime("%A").title(),
                'startTime': day.startTime.strftime("%H:%M"),
                'endTime': day.endTime.strftime("%H:%M"),
                'breakTime': day.breakTime.strftime("%H:%M"),
                'workTime': day.workTime.strftime("%H:%M"),
            })

        return timesheetObject

    def getTimesheetTotalWorkMinutesForTemplate(self):
        workTimeH = self.totalWorkMinutes / 60
        workTimeM = self.totalWorkMinutes % 60
        totalTimeForContext = str("%02d" % (workTimeH,)) + ':' + str("%02d" % (workTimeM,))

        return totalTimeForContext

    def getTimesheetStatus(self):
        return self.TimesheetStatus[self.timesheetStatus].label

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Absence(models.Model):
    class AbsenceTypes(models.TextChoices):
        VACATIONP = 'VACATIONP', _('Vacation leave paid')
        VACATIONNP = 'VACATIONNP', _('Vacation leave not paid')
        ONDEMAND = 'ONDEMAND', _('On demand')
        SICKLEAVE = 'SICKLEAVE', _('Sick leave')

    class StatusTypes(models.TextChoices):
        SENTTOAPPROVE = 'SENTTOAPPROVE', _('Sent to approve')
        DECLINED = 'DECLINED', _('Declined')
        APPROVED = 'APPROVED', _('Approved')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='absenceOwner', default=None, blank=True,
                              on_delete=models.CASCADE)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='absenceManager', default=None, blank=True,
                                on_delete=models.CASCADE)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    absenceType = models.CharField(
        max_length=17,
        choices=AbsenceTypes.choices,
        default=AbsenceTypes.VACATIONP,
    )
    statusType = models.CharField(
        max_length=17,
        choices=StatusTypes.choices,
        default=StatusTypes.SENTTOAPPROVE,
    )
    workDays = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        self.objectName = str(self.owner.username) + "-" + str(self.startDate) + "-" + str(self.endDate)
        return self.objectName

    def getAbsenceRequestType(self):
        return self.AbsenceTypes[self.absenceType].label

    def getAbsenceRequestStatus(self):
        return self.StatusTypes[self.statusType].label

    def getStartDateForTemplate(self):
        return str(self.startDate.strftime("%d %B, %Y").title())

    def getEndDateForTemplate(self):
        return str(self.endDate.strftime("%d %B, %Y").title())

def getAbsenceTypesForTemplate():
    absenceTypes = []
    for absenceType in Absence.AbsenceTypes.choices:
        absenceTypes.append({
            'absenceValue': absenceType[0],
            'absenceDescription': absenceType[1],
        })
    return absenceTypes

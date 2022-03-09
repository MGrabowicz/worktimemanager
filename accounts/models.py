from django.contrib.auth.models import User
from django.db import models

from teams.models import Team


class wtmUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='group', default=None, blank=True, null=True, on_delete=models.CASCADE)
    isEmailVerified = models.BooleanField(default=False)
    promotedToManager = models.BooleanField(default=False)
    personalStartTime = models.TimeField(default="08:00", null=True)
    personalEndTime = models.TimeField(default="16:25",null=True)
    personalBreakTime = models.TimeField(default="00:25",null=True)

    def __str__(self):
        return self.user.username

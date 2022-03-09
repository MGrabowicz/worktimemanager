from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False, unique=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='manager', default=None, blank=True,
                                on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users', default=None, blank=True)

    def __str__(self):
        return self.name

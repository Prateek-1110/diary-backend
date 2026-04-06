from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True)
    theme = models.CharField(max_length=50, default='default')
    font = models.CharField(max_length=50, default='lora')
    last_seen_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
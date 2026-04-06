import uuid
from django.db import models
from django.conf import settings

class FutureLetter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='letters')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    unlocks_at = models.DateTimeField(db_index=True)
    is_unlocked = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['unlocks_at']